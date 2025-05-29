CREATE_TABLE_TASKS = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task TEXT NOT NULL,
    completed INTEGER DEFAULT 0,
    created_at TEXT NOT NULL
)
"""

SELECT_TASKS = "SELECT id, task, completed, created_at FROM tasks"
SELECT_completed = "SELECT id, task, created_at FROM tasks WHERE completed = 1"
SELECT_uncompleted = "SELECT id, task, created_at FROM tasks WHERE completed = 0"

INSERT_TASK = "INSERT INTO tasks (task, created_at) VALUES (?, ?)"
UPDATE_TASK = 'UPDATE tasks SET task = ? WHERE id = ?'
DELETE_TASK = "DELETE FROM tasks WHERE id = ?"
