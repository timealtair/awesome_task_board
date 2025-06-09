import sqlite3
import sys
import logging
from utils.db_functions import (
    get_existing_tables, get_status_from_user,
)


DEFAULT_STATUS_SET = dict.fromkeys((
    'todo',
    'in progress',
    'done',
))


def show_table_selection(tables):
    print('Existing tables:')
    for idx, table in enumerate(tables, start=1):
        print(f'{idx}. {table}')
    while True:
        try:
            choice = int(input('Choose a table by number: '))
            if 1 <= choice <= len(tables):
                return tables[choice - 1]
        except ValueError:
            pass
        logging.error('Invalid selection. Try again.')


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


def main(db_file):
    conn = sqlite3.connect(db_file)
    try:
        args = parse_args(sys.argv)

        if args['table']:
            table = args['table']
        else:
            tables = get_existing_tables(conn)
            if not tables:
                print(
                    'No existing tables found. Please enter a name '
                    'to create a new task table.'
                )
                table = input('Enter table name: ').strip()
            else:
                table = show_table_selection(tables)

        task = args['task'] or input('Enter task: ').strip()
        status = args['status'] or get_status_from_user(
            table, conn, DEFAULT_STATUS_SET
        )

        insert_task(conn, table, task, status)

    finally:
        conn.close()


if __name__ == '__main__':
    import readline

    db_file = r'./database/todo.db'
    try:
        main(db_file)
    except (EOFError, KeyboardInterrupt):
        pass
