def echo():
    from pyfaasm.core import get_input_len, read_input, write_output

    input_len = get_input_len()
    if input_len == 0:
        write_output("Nothing to echo")
        return

    input_data: bytes = read_input(input_len)
    input_data_str = input_data.decode("utf-8")

    print(f"Input string: {input_data_str!r}")
    write_output(input_data_str.encode(encoding="utf-8"))


def faasm_main() -> int:
    echo()
    return 0
