import sqlite3
from pathlib import Path


class Database:
    """Handles low-level SQLite database connections."""

    def __init__(self, db_name="tasktify.db"):
        self.db_path = Path(db_name)
        self.connection = sqlite3.connect(str(self.db_path))
        self.connection.row_factory = sqlite3.Row
        self.connection.execute("PRAGMA foreign_keys = ON;")
        self.create_tables()

    def create_tables(self):
        # 1. Users table for authentication
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        # 2. Tasks table with user_id foreign key
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT DEFAULT '',
                category TEXT NOT NULL,
                priority TEXT NOT NULL,
                due_date TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        """)

        # Migration safety: Ensure user_id column exists if updating an existing DB
        try:
            self.connection.execute("ALTER TABLE tasks ADD COLUMN user_id INTEGER DEFAULT 1;")
        except sqlite3.OperationalError:
            pass

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