import sqlite3
import sys
import logging
import readline
from os import PathLike


def get_table_name():
    if len(sys.argv) > 1:
        return sys.argv[1]
    return input('Enter table name: ').strip()


def create_table(
    db_file: str | PathLike,
    table_name: str | PathLike,
    schema_file: str | PathLike,
):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        with open(schema_file) as f:
            sql_script = f.read()
        cursor.executescript(
            sql_script.format(table_name=table_name)
        )
        conn.commit()
    except Exception as e:
        logging.error('Error creating table: %s', e)
    finally:
        conn.close()


if __name__ == '__main__':
    db_file = r'./database/todo.db'
    schema_file = r'./database/todo_schema.sql'

    try:
        table_name = get_table_name()
        if table_name:
            create_table(db_file, table_name, schema_file)
        else:
            logging.error('No table name provided.')
    except (EOFError, KeyboardInterrupt):
        pass
