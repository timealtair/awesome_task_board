import sqlite3
from os import PathLike
from utils.db_functions import (
    get_table_from_user, get_status_from_user, get_items_by_status,
)
from utils.prettify_functions import print_separator
from settings.default_status_set import DEFAULT_STATUS_SET


def modify_iter(table: str, conn: sqlite3.Connection):
    status = get_status_from_user(table, conn, DEFAULT_STATUS_SET)
    print(get_items_by_status(table, status, conn))


def main(db_file: str | PathLike, sep_symbol: str):
    try:
        conn = sqlite3.Connection(db_file)

        print_separator(sep_symbol)
        table = get_table_from_user(conn)

        while True:
            modify_iter(table, conn)
    finally:
        conn.close()


if __name__ == '__main__':
    import readline

    db_file = r'./database/todo.db'
    separator = '`'

    try:
        main(db_file, separator)
    except (EOFError, KeyboardInterrupt):
        pass
