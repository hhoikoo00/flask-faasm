import os
from pathlib import Path

CPYTHON_WASM_FILE = Path(os.getenv("CPYTHON_WASM_FILE", default="./data/cpython.wasm"))
CPYTHON_USER = "python"
CPYTHON_FUNC = "py_func"

FAASM_FUNC_TEMPLATE_FILE = Path(os.getenv("FAASM_FUNC_TEMPLATE", default="./data/faasm.template.py"))
