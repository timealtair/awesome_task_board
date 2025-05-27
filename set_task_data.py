import sqlite3
import sys


def get_existing_tables(conn):
    cursor = conn.cursor()
    cursor.execute(
        'SELECT name FROM sqlite_master '
        "WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    return [row[0] for row in cursor.fetchall()]


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
        print('Invalid selection. Try again.')


def insert_task(conn, table, task, status):
    cursor = conn.cursor()
    cursor.execute(
        f"INSERT INTO '{table}' (task, status) VALUES (?, ?)",
        (task, status)
    )
    conn.commit()


def parse_args(argv):
    args = {'table': None, 'task': None, 'status': 'todo'}
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
        status = args['status'] or input(
            'Enter status (default: todo): '
        ).strip() or 'todo'

        insert_task(conn, table, task, status)

    finally:
        conn.close()


if __name__ == '__main__':
    db_file = r'./database/todo.db'
    try:
        main(db_file)
    except (EOFError, KeyboardInterrupt):
        pass
