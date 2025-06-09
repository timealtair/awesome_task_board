import sqlite3
import sys
from utils.db_functions import (
    get_table_from_user, get_status_from_user,
)
from utils.prettify_functions import print_separator


DEFAULT_STATUS_SET = dict.fromkeys((
    'todo',
    'in progress',
    'done',
))


def insert_task(conn, table, task, status):
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO '{table}' (task, status) VALUES (?, ?)",
        (task, status)
    )
    conn.commit()


def parse_args(argv):
    args = {'table': None, 'task': None, 'status': None}
    if len(argv) > 1:
        args['table'] = argv[1]
    if len(argv) > 2:
        args['task'] = argv[2]
    if len(argv) > 3:
        args['status'] = argv[3]
    return args


def main(db_file, separator):
    conn = sqlite3.connect(db_file)
    try:
        args = parse_args(sys.argv)

        if args['table']:
            table = args['table']
        else:
            print_separator(separator)
            table = get_table_from_user(conn)

        if args['task']:
            task = args['task']
        else:
            print_separator(separator)
            task = input('Enter task: ').strip()

        if args['status']:
            status = args['status']
        else:
            print_separator(separator)
            status = get_status_from_user(
                table, conn, DEFAULT_STATUS_SET
            )

        insert_task(conn, table, task, status)

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
