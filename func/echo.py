def echo():
    from pyfaasm.core import get_input_len, read_input, write_output

    input_len = get_input_len()
    if input_len == 0:
        write_output("Nothing to echo")
        return 0

    input_data: bytes = read_input(input_len)
    input_data_str = input_data.decode("utf-8")

    write_output(f"Input bytes: {input_data!r}")
    write_output(f"Input string: {input_data_str!r}")

    return 0
