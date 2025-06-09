import sqlite3
from os import PathLike
from utils.db_functions import (
    get_table_from_user, get_status_from_user, get_task_id_from_user,
    get_modify_or_delete_selection, delete_task, modify_task,
)
from utils.prettify_functions import print_separator
from settings.default_status_set import DEFAULT_STATUS_SET


def modify_iter(table: str, conn: sqlite3.Connection, sep_symbol: str):
    print_separator(sep_symbol)
    status = get_status_from_user(table, conn, DEFAULT_STATUS_SET)

    print_separator(sep_symbol)
    idx, tasks, schema = get_task_id_from_user(table, status, conn)
    if idx is None:
        return
    print_separator(sep_symbol)
    mod_or_del = get_modify_or_delete_selection()
    match mod_or_del:
        case 0:
            print_separator(sep_symbol)
            print('Select new status: ')
            print_separator(sep_symbol)
            status = get_status_from_user(table, conn, DEFAULT_STATUS_SET)
            modify_task(table, idx, status, conn)
        case 1:
            delete_task(tasks, idx, table, conn)
        case _:
            raise RuntimeError(
                'get_modify_or_delete_selection return not 0 1!'
            )


def main(db_file: str | PathLike, sep_symbol: str):
    try:
        conn = sqlite3.Connection(db_file)

        print_separator(sep_symbol)
        table = get_table_from_user(conn)

        while True:
            modify_iter(table, conn, sep_symbol)
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
