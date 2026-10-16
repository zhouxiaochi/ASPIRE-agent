from __future__ import annotations
import argparse
from typing import Any
from .com.dispatch import execute
from .com.session import SessionStore

def _key(payload: dict[str, Any]) -> str: return str(payload.get("task_hash") or payload["task_key"])

def create_app(store: SessionStore | None = None) -> Any:
    try: from fastapi import FastAPI, HTTPException
    except ImportError as exc: raise RuntimeError("Install asipre-agent[server]") from exc
    app = FastAPI(title="ASIPRE Agent Aspen Service"); store = store or SessionStore(_windows_factory)
    @app.get("/health")
    def health(): return {"status": "ok", "active_sessions": len(store.sessions)}
    @app.post("/session/start")
    def start(payload: dict[str, Any]):
        key = _key(payload); store.start(key, payload.get("initial_bkp"), payload.get("show_gui")); return {"status": "started", "task_hash": key}
    def load_impl(payload: dict[str, Any]):
        store.get(_key(payload)).document.InitFromArchive2(str(payload.get("bkp_path") or payload["path"])); return {"status": "loaded"}
    app.post("/session/load_bkp")(load_impl); app.post("/session/load")(load_impl)
    @app.post("/session/checkpoint")
    def checkpoint(payload: dict[str, Any]):
        session = store.get(_key(payload)); filename = payload.get("filename") or payload.get("path") or f"{_key(payload)}.bkp"
        if session.checkpoint: return session.checkpoint(filename)
        session.document.SaveAs(str(filename)); return {"status": "saved", "path": str(filename)}
    @app.post("/session/close")
    def close(payload: dict[str, Any]): store.remove(_key(payload), False); return {"status": "closed"}
    def operation_impl(payload: dict[str, Any]):
        try:
            result = execute(store.get(_key(payload)).document, str(payload["operation"]), dict(payload.get("parameters", {})))
            return result if isinstance(result, dict) else {"result": result}
        except Exception as exc: raise HTTPException(status_code=400, detail=str(exc)) from exc
    app.post("/session/execute")(operation_impl); app.post("/execute")(operation_impl)
    return app

def _windows_factory(initial_bkp: str | None, show_gui: bool | None) -> Any:
    try: import win32com.client
    except ImportError as exc: raise RuntimeError("Install the Windows extra and run with Aspen Plus") from exc
    document = win32com.client.Dispatch("Apwn.Document")
    if show_gui is not None: document.Visible = show_gui
    document.InitFromArchive2(initial_bkp) if initial_bkp else document.InitNew2()
    return document

def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--host", default="127.0.0.1"); parser.add_argument("--port", default=5000, type=int); args = parser.parse_args()
    try: import uvicorn
    except ImportError as exc: raise RuntimeError("Install asipre-agent[server]") from exc
    uvicorn.run(create_app(), host=args.host, port=args.port); return 0
