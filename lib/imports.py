import ast
from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Name:
    name: str
    alias: str | None = None

    def __str__(self) -> str:
        alias_str = "" if self.alias is None else f" as {self.alias}"
        return f"{self.name}{alias_str}"


@dataclass(frozen=True, kw_only=True)
class Import:
    name: Name

    def __str__(self) -> str:
        return f"import {self.name}"


@dataclass(frozen=True, kw_only=True)
class ImportFrom:
    module: str
    subimport: Import

    def __str__(self) -> str:
        return f"from {self.module} {self.subimport}"


class ImportVisitor(ast.NodeVisitor):
    def __init__(self) -> None:
        super().__init__()

        self.imports: set[Import | ImportFrom] = set()

    def visit_Import(self, node: ast.Import) -> None:
        for name in node.names:
            import_obj = Import(name=Name(name=name.name, alias=name.asname))
            self.imports.add(import_obj)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        # Ignore relative imports of form `from . import ...`.
        if node.module is None:
            return
        # Ignore relative submodule imports of form `from .submodule import ...`.
        if node.level > 0:
            return

        for name in node.names:
            import_obj = ImportFrom(module=node.module, subimport=Import(name=Name(name=name.name, alias=name.asname)))
            self.imports.add(import_obj)
