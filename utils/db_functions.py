import sys
import sqlite3


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
    print('You selected status:', status)
