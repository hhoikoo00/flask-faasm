import os
from pathlib import Path

CPYTHON_WASM_FILE = Path(os.getenv("CPYTHON_WASM_FILE", default="./data/cpython.wasm"))
