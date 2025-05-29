import sqlite3
from db import queries
from config import db_path
from datetime import datetime

def init_db():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_TABLE_TASKS)

    conn.commit()
    conn.close()

def get_tasks(filter_type='all'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # cursor.execute(queries.SELECT_TASKS)

    if filter_type == 'completed':
        cursor.execute(queries.SELECT_completed)
    elif filter_type == 'uncompleted':
        cursor.execute(queries.SELECT_uncompleted)
    else:
        cursor.execute(queries.SELECT_TASKS)

    tasks = cursor.fetchall()
    conn.close()
    return tasks

# def get_tasks():
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute(queries.SELECT_TASKS)
#     tasks = cursor.fetchall()
#     conn.close()
#     return tasks


def add_task_db(task):
    from datetime import datetime
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(queries.INSERT_TASK, (task, created_at))
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id, created_at


def update_task_db(task_id, new_task, completed=None):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # cursor.execute(queries.UPDATE_TASK, (new_task, task_id))

    if new_task is not None:
        cursor.execute("UPDATE tasks SET task = ? WHERE id = ?", (new_task, task_id))
        
    if completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))

    conn.commit()
    conn.close()

# def update_task_db(task_id, new_task):
#     conn = sqlite3.connect(db_path)
#     cursor = conn.cursor()
#     cursor.execute(queries.UPDATE_TASK, (new_task, task_id))
#     conn.commit()
#     conn.close()


def delete_task_db(task_id):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id,))
    conn.commit()
    conn.close()