import sqlite3
import sys
import logging


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


def get_status_from_user():
    print('Choose a status:')
    print('1. todo (default)')
    print('2. in progress')
    print('3. done')
    print('4. custom')

    while True:
        try:
            choice = input('Enter your choice (1-4): ').strip()
            if not choice:
                return 'todo'
            choice = int(choice)

            if choice == 1:
                return 'todo'
            elif choice == 2:
                return 'in progress'
            elif choice == 3:
                return 'done'
            elif choice == 4:
                custom_status = input('Enter custom status: ').strip()
                if not custom_status:
                    return 'todo'
                return custom_status
            else:
                logging.error(
                    'Invalid choice. Please enter a number between 1 and 4.'
                )

        except ValueError:
            logging.error('Invalid input. Please enter a number.')


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
        status = args['status'] or get_status_from_user()

        insert_task(conn, table, task, status)

    finally:
        conn.close()


if __name__ == '__main__':
    db_file = r'./database/todo.db'
    try:
        main(db_file)
    except (EOFError, KeyboardInterrupt):
        pass
