CREATE TABLE '{table_name}' (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    status TEXT DEFAULT 'todo',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modify_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TRIGGER 'update_{table_name}_modify_time'
AFTER UPDATE ON '{table_name}'
FOR EACH ROW
BEGIN
    UPDATE '{table_name}' SET modify_time = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;
