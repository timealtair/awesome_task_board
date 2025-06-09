

def get_existing_tables(conn):
    cursor = conn.cursor()
    cursor.execute(
        'SELECT name FROM sqlite_master '
        "WHERE type='table' AND name NOT LIKE 'sqlite_%';"
    )
    return [row[0] for row in cursor.fetchall()]
