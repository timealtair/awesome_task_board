import sqlite3


def _get_and_parse_results(query: str, conn: sqlite3.Connection) -> list:
    cursor = conn.cursor()
    cursor.execute(query)
    return [row[0] for row in cursor.fetchall()]


def get_existing_tables(conn: sqlite3.Connection) -> list:
    query = (
        'SELECT name FROM sqlite_master '
        "WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    return _get_and_parse_results(query, conn)


def get_existing_status_set(table_name: str, conn: sqlite3.Connection) -> set:
    query = f'select status from `{table_name}`'
    return set(_get_and_parse_results(query, conn))


if __name__ == '__main__':
    import readline

    db_file = r'./database/todo.db'

    conn = sqlite3.Connection(db_file)
    print('Found tables:')
    print(get_existing_tables(conn))
    table = input('Enter table name: ')
    print('Found statuses:')
    print(get_existing_status_set(table, conn))
