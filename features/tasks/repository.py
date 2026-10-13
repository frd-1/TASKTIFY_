from database.database import Database
from features.tasks.model import Task


class TaskRepository:
    """Handles task SQL queries scoped by user_id."""

    def __init__(self, db: Database):
        self.db = db

    def add(self, user_id, title, description, category, priority, due_date, status):
        cursor = self.db.execute_query("""
            INSERT INTO tasks (user_id, title, description, category, priority, due_date, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, title, description, category, priority, due_date, status))
        return cursor.lastrowid

    def get_all(self, user_id):
        rows = self.db.fetch_all("""
            SELECT * FROM tasks
            WHERE user_id = ?
            ORDER BY due_date ASC, id DESC
        """, (user_id,))
        return [Task.from_row(row) for row in rows]

    def get_by_id(self, task_id, user_id):
        row = self.db.fetch_one("""
            SELECT * FROM tasks WHERE id = ? AND user_id = ?
        """, (task_id, user_id))
        if row:
            return Task.from_row(row)
        return None

    def update(self, task_id, user_id, title, description, category, priority, due_date, status):
        cursor = self.db.execute_query("""
            UPDATE tasks
            SET title = ?, description = ?, category = ?, priority = ?, due_date = ?, status = ?
            WHERE id = ? AND user_id = ?
        """, (title, description, category, priority, due_date, status, task_id, user_id))
        return cursor.rowcount > 0

    def delete(self, task_id, user_id):
        cursor = self.db.execute_query("""
            DELETE FROM tasks WHERE id = ? AND user_id = ?
        """, (task_id, user_id))
        return cursor.rowcount > 0