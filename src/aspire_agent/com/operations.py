from __future__ import annotations
from typing import Any, Iterator

class OperationError(RuntimeError): pass

def _node(tree: Any, path: str) -> Any:
    node = tree.FindNode(path)
    if node is None: raise OperationError(f"Aspen tree path not found: {path}")
    return node

def _add(tree: Any, path: str, token: str) -> None:
    elements = _node(tree, path).Elements
    result = elements.Add(token)
    if result is False: raise OperationError(f"Aspen rejected creation token: {token}")

def create_material_stream(tree: Any, stream_name: str) -> dict[str, str]:
    _add(tree, r"Data\Streams", f"{stream_name}!MATERIAL")
    return {"stream_name": stream_name, "stream_type": "MATERIAL"}

def create_heat_stream(tree: Any, stream_name: str) -> dict[str, str]:
    _add(tree, r"Data\Streams", f"{stream_name}!HEAT")
    return {"stream_name": stream_name, "stream_type": "HEAT"}

def create_mixer_block(tree: Any, block_name: str) -> dict[str, str]:
    _add(tree, r"Data\Blocks", f"{block_name}!MIXER")
    return {"block_name": block_name, "block_type": "MIXER"}

def create_heater_block(tree: Any, block_name: str) -> dict[str, str]:
    _add(tree, r"Data\Blocks", f"{block_name}!HEATER")
    return {"block_name": block_name, "block_type": "HEATER"}

def _items(collection: Any) -> Iterator[Any]:
    count = int(getattr(collection, "Count", 0))
    seen: set[int] = set()
    for index in list(range(count)) + list(range(1, count + 1)):
        try: item = collection.Item(index)
        except Exception: continue
        if item is not None and id(item) not in seen:
            seen.add(id(item)); yield item

def _name(item: Any) -> str:
    return str(getattr(item, "Name", getattr(item, "name", "")))

def _ports(tree: Any, block_name: str) -> Any:
    block = _node(tree, f"Data\\Blocks\\{block_name}")
    ports = getattr(block, "Ports", None)
    if ports is None:
        port_node = tree.FindNode(f"Data\\Blocks\\{block_name}\\Ports")
        ports = getattr(port_node, "Elements", None) if port_node is not None else None
    if ports is None: raise OperationError(f"Block has no live Ports collection: {block_name}")
    return ports

def _port(tree: Any, block_name: str, port_name: str) -> Any:
    ports = _ports(tree, block_name)
    for port in _items(ports):
        if _name(port) == port_name: return port
    try: return ports.Item(port_name)
    except Exception as exc: raise OperationError(f"Port {port_name} is not exposed by block {block_name}") from exc

def _connections(port: Any) -> list[str]:
    elements = getattr(port, "Elements", None)
    if elements is None: return []
    return [_name(item) for item in _items(elements) if _name(item)]

def list_block_ports(tree: Any, block_name: str) -> dict[str, Any]:
    result = []
    for port in _items(_ports(tree, block_name)):
        result.append({"name": _name(port), "direction": str(getattr(port, "Direction", "")), "kind": str(getattr(port, "Kind", "MATERIAL")), "connected_streams": _connections(port)})
    return {"block_name": block_name, "ports": result}

def connect_stream(tree: Any, block_name: str, stream_name: str, port_name: str) -> dict[str, Any]:
    port = _port(tree, block_name, port_name)
    elements = getattr(port, "Elements", None)
    if elements is None: raise OperationError(f"Port has no connection Elements: {block_name}.{port_name}")
    elements.Add(stream_name)
    connected = _connections(port)
    if stream_name not in connected: raise OperationError(f"Connection readback failed: {stream_name}")
    return {"block_name": block_name, "stream_name": stream_name, "port_name": port_name, "connected_streams": connected}
