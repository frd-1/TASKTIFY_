import sqlite3
from pathlib import Path


class Database:
    """Handles low-level SQLite database connections."""

    def __init__(self, db_name="tasktify.db"):
        self.db_path = Path(db_name)
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending'
            )
        """)
        self.connection.commit()

    def execute_query(self, query, params=()):
        cursor = self.connection.execute(query, params)
        self.connection.commit()
        return cursor

    def fetch_all(self, query, params=()):
        cursor = self.connection.execute(query, params)
        return cursor.fetchall()

    def fetch_one(self, query, params=()):
        cursor = self.connection.execute(query, params)
        return cursor.fetchone()

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None