import hashlib
import logging
from base64 import b64encode
from pathlib import Path
from typing import Any

import requests
from faasmtools.endpoints import get_faasm_invoke_host_port, get_faasm_upload_host_port

logger = logging.getLogger(__name__)


UPLOAD_HOST, UPLOAD_PORT = get_faasm_upload_host_port()
INVOKE_HOST, INVOKE_PORT = get_faasm_invoke_host_port()
FAASM_OUTPUT_TEXT_SEP = "Python call succeeded\n\n"


def upload_func(wasm_file_path: Path, user: str, fn_name: str) -> None:
    upload_url = f"http://{UPLOAD_HOST}:{UPLOAD_PORT}/f/{user}/{fn_name}"

    # Upload the function to Faasm.
    logger.info(f"Uploading function '{user}/{fn_name}' to {upload_url!r}...")
    with open(wasm_file_path, "rb") as wasm_file:
        res = requests.put(upload_url, data=wasm_file)

    # Handle error if the upload request fails.
    res.raise_for_status()

    logger.info("Upload successful!")
    logger.debug(f"Upload response: {res.text!r}")


def upload_py_func(source: str, fn_name: str | None = None) -> str:
    # Provide a default function name if none provided. Use the hash code of function's source.
    if fn_name is None:
        fn_name = hashlib.sha256(source.encode()).hexdigest()[:32]

    upload_url = f"http://{UPLOAD_HOST}:{UPLOAD_PORT}/p/python/{fn_name}"

    # Upload the Python function to Faasm.
    logger.info(f"Uploading Python function {fn_name!r} to {upload_url!r}...")
    res = requests.put(upload_url, data=source)

    # Handle error if the upload request fails.
    res.raise_for_status()

    logger.info("Upload successful!")
    logger.debug(f"Upload response: {res.text!r}")

    return fn_name


def encode_input(input_data: str) -> str:
    # The input data field must be base64 encoded.
    return b64encode(input_data.encode(encoding="utf-8")).decode(encoding="utf-8")


def extract_output(result_text: str) -> str:
    _, output = result_text.split(FAASM_OUTPUT_TEXT_SEP, maxsplit=1)
    return output


def invoke_py_func(fn_name: str, input_data: Any | None = None) -> Any:
    # Prepare invoke data. Include input data if input data provided.
    invoke_data = {
        "async": False,
        "user": "python",
        "function": "py_func",
        "python": True,
        "py_user": "python",
        "py_func": fn_name,
    }
    if input_data is not None:
        invoke_data["input_data"] = input_data

    invoke_url = f"http://{INVOKE_HOST}:{INVOKE_PORT}"

    # Invoke the uploaded function.
    logger.info(f"Invoking Python function {fn_name!r} with arguments: ({input_data!r})...")
    res = requests.post(invoke_url, json=invoke_data)

    # Handle error if the invoke request fails.
    res.raise_for_status()

    logger.info("Invoke successful!")
    logger.debug(f"Invoke Response [{res.status_code}]: {res.text!r}")

    # Extract the output produced by `write_output()` function.
    output = extract_output(res.text)

    return output
