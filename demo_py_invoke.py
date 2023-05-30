import argparse
import logging
from pathlib import Path
from time import sleep

from lib.faasm import invoke_py_func, upload_cpython_runtime, upload_py_func

logger = logging.getLogger(__name__)

INVOKE_DELAY = 2


def test_upload_invoke_simple_func(fn_file: Path, input_data: str) -> None:
    upload_cpython_runtime()

    # Read the Python function file at `fn_file` and upload the parsed Python function.
    fn_name = upload_py_func(fn_file.read_text(encoding="utf-8"))

    logger.info(f"Waiting for {INVOKE_DELAY} seconds for the upload to be propagated...")
    sleep(INVOKE_DELAY)

    # Invoke uploaded function.
    output = invoke_py_func(fn_name, input_data=input_data)
    logger.info(f"Output: {output!r}")


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Parse command-line arguments.
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("-f", "--file", type=str, default="./func/echo.py", help="Python source file to upload")
    arg_parser.add_argument(
        "-i", "--input", type=str, default="Hello, Faasm!", help="Input to the function to be tested"
    )
    args = arg_parser.parse_args()

    func_file = Path(args.file)
    if not func_file.is_file():
        error_msg = f"Provided file {func_file!r} does not exist!"
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    input_data: str = args.input

    # Run the test.
    test_upload_invoke_simple_func(func_file, input_data)


if __name__ == "__main__":
    main()
