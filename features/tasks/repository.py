from database.database import Database
from features.tasks.model import Task


class TaskRepository:
    """Handles task SQL queries and direct database interaction."""

    def __init__(self, db: Database):
        self.db = db

    def add(self, title, description, category, priority, due_date, status):
        cursor = self.db.execute_query("""
            INSERT INTO tasks (title, description, category, priority, due_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, description, category, priority, due_date, status))
        return cursor.lastrowid

    def get_all(self):
        rows = self.db.fetch_all("""
            SELECT * FROM tasks
            ORDER BY due_date ASC, id DESC
        """)
        return [Task.from_row(row) for row in rows]

    def get_by_id(self, task_id):
        row = self.db.fetch_one("""
            SELECT * FROM tasks WHERE id = ?
        """, (task_id,))
        if row:
            return Task.from_row(row)
        return None

    def update(self, task_id, title, description, category, priority, due_date, status):
        cursor = self.db.execute_query("""
            UPDATE tasks
            SET title = ?, description = ?, category = ?, priority = ?, due_date = ?, status = ?
            WHERE id = ?
        """, (title, description, category, priority, due_date, status, task_id))
        return cursor.rowcount > 0

    def delete(self, task_id):
        cursor = self.db.execute_query("""
            DELETE FROM tasks WHERE id = ?
        """, (task_id,))
        return cursor.rowcount > 0