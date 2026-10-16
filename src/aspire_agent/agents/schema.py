from __future__ import annotations
import ast
import re
from dataclasses import dataclass
from pathlib import PurePosixPath

@dataclass(frozen=True)
class FileEdit:
    path: str
    content: str

@dataclass(frozen=True)
class EditBundle:
    files: tuple[FileEdit, ...]
    summary: str = ""

_HEADER = re.compile(r"^---FILE: (.+)---$", re.MULTILINE)

def parse_edit_bundle(text: str) -> EditBundle:
    matches = list(_HEADER.finditer(text))
    if not matches: raise ValueError("Model output must contain at least one ---FILE: path--- section")
    files = []
    for index, match in enumerate(matches):
        path = match.group(1).strip().replace("\\", "/")
        pure = PurePosixPath(path)
        if pure.is_absolute() or ".." in pure.parts: raise ValueError(f"Unsafe output path: {path}")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        files.append(FileEdit(path, text[match.end():end].strip("\r\n") + "\n"))
    return EditBundle(tuple(files))

def check_python(edit: FileEdit) -> None:
    if edit.path.endswith(".py"): ast.parse(edit.content, filename=edit.path)
