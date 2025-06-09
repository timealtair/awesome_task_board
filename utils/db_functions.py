import sys
import sqlite3
from tabulate import tabulate


ERR_SYMBOL = '!>'


def print_error(message: str):
    print(
        ERR_SYMBOL, message, file=sys.stderr,
    )


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
            print_error('Status should be valid number!')
            continue
        try:
            return status_list[choice]
        except IndexError:
            if choice == custom_num:
                return input('Enter custom status: ')
            else:
                print_error('Status number is out of range!')


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
            print_error('Invalid selection. Try again.')


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
) -> tuple:
    items, schema = _get_items_by_status(table, status, conn)
    if not items:
        print_error('No tasks found')
        return None, None, None
    print('Found tasks:')
    print(tabulate(items, schema))
    while True:
        idx = input('Enter task id: ')
        if not idx.strip():
            return None, None, None
        try:
            idx = int(idx)
        except ValueError:
            print_error('Index should be valid number!')
            continue
        if idx not in (el[0] for el in items):
            print_error('Index is not in avalable tasks!')
            continue
        return idx, items, schema


def get_modify_or_delete_selection():
    """
    modify -> 0 | delete -> 1
    """
    print('Select option:\n0. modify\n1. delete')
    while True:
        choice = input('Enter option number (0): ')
        if not choice.split():
            return 0
        try:
            choice = int(choice)
        except ValueError:
            print_error('Option should be valid number 0 or 1')
            continue
        if choice in (0, 1):
            return choice
        else:
            print_error('Number is out of range 0-1')
            continue


def _delete_task(
    table: str, idx: str, conn: sqlite3.Connection
):
    query = f'DELETE FROM `{table}` where id = {idx}'
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()


def delete_task(
    tasks: list[tuple], idx: str, table: str, conn: sqlite3.Connection
):
    target = None
    for task in tasks:
        if task[0] == idx:
            target = task
    if target is None:
        raise RuntimeError("target task shouldn't be None!")
    print('Task for deletion:', task, sep='\n')
    while True:
        choice = input('Are you sure? (yes/no): ').strip()
        if not choice:
            continue
        if choice.lower() in 'yes':
            _delete_task(table, idx, conn)
        elif choice.lower() not in 'no':
            continue
        return


def modify_task():
    pass


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
