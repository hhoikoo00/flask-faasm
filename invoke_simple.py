import argparse
import logging
from pathlib import Path
from time import sleep

from lib.constants import CPYTHON_WASM_FILE
from lib.faasm import invoke_py_func, upload_func, upload_py_func

logger = logging.getLogger(__name__)


def test_upload_invoke_simple_func(fn_file: Path) -> None:
    # Upload the CPython runtime.
    upload_func(CPYTHON_WASM_FILE, user="python", fn_name="py_func")

    # Read the Python function file at `fn_file` and get its source.
    with open(fn_file, "r", encoding="utf-8") as file:
        fn_source = file.read()

    # Upload the parsed Python function.
    fn_name = upload_py_func(fn_source)

    # Sleep for 2 seconds for upload to be propagated.
    sleep(2)

    # Function invocation arguments.
    input_data = "Hello Faasm"

    # Invoke uploaded function.
    invoke_py_func(fn_name, input_data=input_data)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Parse command-line arguments.
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument(
        "-f", "--file", type=str, default="./func/echo.py", help="Python source file to upload"
    )
    args = arg_parser.parse_args()

    func_file = Path(args.file)
    if not func_file.is_file():
        error_msg = f"Provided file {func_file!r} does not exist!"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)

    # Run the test.
    test_upload_invoke_simple_func(func_file)


if __name__ == "__main__":
    main()
