import json
import typing as t

from pyfaasm.core import get_input_len, read_input, write_output

{__request_def}


request = None


{__function}


def faasm_main() -> int:
    # Read input (as bytes) and parse as JSON.
    input_len = get_input_len()
    assert input_len > 0
    input_data_json = read_input(input_len)
    input_data = json.loads(input_data_json)

    # Obtain the function args and kwargs from the input data.
    args = input_data["func_args"]["args"]
    kwargs = input_data["func_args"]["kwargs"]

    # Initialize input request object from values of input.
    request_data = input_data["request_data"]
    global request
    request = Request(**request_data)

    # Call the provided function.
    output = {__function_name}(*args, **kwargs)

    # Format the output in JSON.
    # TODO: Alternatively in some byte format?
    output_json = json.dumps(output)

    # Encode the output in bytes and output the function result to Faasm.
    write_output(output_json.encode(encoding="utf-8"))

    return 0
