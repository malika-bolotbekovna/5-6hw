CREATE_TABLE_TASKS = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        created_at TEXT,
        completed INTEGER DEFAULT 0
    )
"""

SELECT_TASKS = "SELECT id, task, created_at FROM tasks"
INSERT_TASK = "INSERT INTO tasks (task, created_at) VALUES (?, ?)"
UPDATE_TASK = "UPDATE tasks SET task = ? WHERE id = ?"
DELETE_TASK = "DELETE FROM tasks WHERE id = ?"
