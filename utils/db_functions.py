import sys
import sqlite3
from tabulate import tabulate


ERR_SYMBOL = '!>'


def _get_and_parse_results(query: str, conn: sqlite3.Connection) -> list:
    cursor = conn.cursor()
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]


def _get_existing_tables(conn: sqlite3.Connection) -> list:
    query = (
        'SELECT name FROM sqlite_master '
        "WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    return _get_and_parse_results(query, conn)


def _get_existing_status_set(table_name: str, conn: sqlite3.Connection) -> set:
    query = f'select status from `{table_name}`'
    return set(_get_and_parse_results(query, conn))


def get_status_from_user(
    table: str, conn: sqlite3.Connection, default_status_set: dict,
) -> str:
    existed_status_set = _get_existing_status_set(table, conn)
    default_status_set.update(
        dict.fromkeys(existed_status_set)
    )
    status_list = list(default_status_set)
    print('Available status list:')
    for num, status in enumerate(status_list):
        print(f'{num}. {status}')
    custom_num = len(status_list)
    print(f'{custom_num}. custom')
    while True:
        choice = input('Enter your status number (0): ')
        if not choice.strip():
            choice = 0
        try:
            choice = int(choice)
        except ValueError:
            print(
                ERR_SYMBOL, 'Status should be valid number!',
                file=sys.stderr,
            )
            continue
        try:
            return status_list[choice]
        except IndexError:
            if choice == custom_num:
                return input('Enter custom status: ')
            else:
                print(
                    ERR_SYMBOL, 'Status number is out of range!',
                    file=sys.stderr,
                )


def get_table_from_user(conn: sqlite3.Connection) -> str:
    tables = _get_existing_tables(conn)
    print('Existing tables:')
    for num, table in enumerate(tables):
        print(f'{num}. {table}')
    while True:
        try:
            choice = int(input('Choose a table by number: '))
            return tables[choice]
        except (ValueError, IndexError):
            print(
                ERR_SYMBOL, 'Invalid selection. Try again.',
                file=sys.stderr,
            )


def _get_keys_from_result_cursor(cursor: sqlite3.Cursor) -> list[str]:
    return [key[0] for key in cursor.description]


def _get_items_by_status(
    table: str, status: str, conn: sqlite3.Connection
) -> tuple[list[tuple], list[str]]:
    cursor = conn.cursor()
    query = f"SELECT * FROM `{table}` WHERE status = '{status}'"
    cursor.execute(query)
    schema = _get_keys_from_result_cursor(cursor)
    return cursor.fetchall(), schema


def get_task_id_from_user(
    table: str, status: str, conn: sqlite3.Connection
) -> int | None:
    items, schema = _get_items_by_status(table, status, conn)
    if not items:
        print(ERR_SYMBOL, 'No tasks found', file=sys.stderr)
        return None
    print('Found tasks:')
    print(tabulate(items, schema))
    while True:
        try:
            idx = int(input('Enter task id: '))
        except ValueError:
            print(
                ERR_SYMBOL, 'Index should be valid number!',
                file=sys.stderr,
            )
            continue
        if idx not in (el[0] for el in items):
            print(
                ERR_SYMBOL, 'Index is not in avalable tasks!',
                file=sys.stderr,
            )
            continue
        return idx


if __name__ == '__main__':
    import readline

    db_file = r'./database/todo.db'

    DEFAULT_STATUS_SET = dict.fromkeys((
        'todo',
        'in progress',
        'done',
    ))

    conn = sqlite3.Connection(db_file)
    table = get_table_from_user(conn)
    status = get_status_from_user(table, conn, DEFAULT_STATUS_SET)
    idx = get_task_id_from_user(table, status, conn)
    print('Your idx:', idx)
