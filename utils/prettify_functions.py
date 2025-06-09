import os


def print_separator(separotor: str):
    columns, _ = os.get_terminal_size()
    result = ''
    while len(result) < columns:
        result += separotor
    result = result[:columns]
    print(result)


if __name__ == '__main__':
    print_separator('-')
    print_separator('-+')
    print_separator('-+*')
