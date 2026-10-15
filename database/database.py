import sqlite3
from pathlib import Path


class Database:
    """Handles SQLite database connections."""

    def __init__(self, db_name="tasktify.db"):
        # Get the path of the database file.
        self.db_path = Path(db_name)

        # Connect to the SQLite database.
        self.connection = sqlite3.connect(str(self.db_path))

        # Allow database rows to be accessed using column names.
        self.connection.row_factory = sqlite3.Row

        # Enable foreign key constraints.
        self.connection.execute("PRAGMA foreign_keys = ON;")

        # Create the necessary database tables.
        self.create_tables()

    def create_tables(self):
        # 1. Create the users table for authentication.
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        """)

        # 2. Create the tasks table and connect tasks to their users.
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

        # Add the user_id column to an existing tasks table if needed.
        try:
            self.connection.execute("ALTER TABLE tasks ADD COLUMN user_id INTEGER DEFAULT 1;")
        except sqlite3.OperationalError:
            # Do nothing if the column already exists or the operation fails.
            pass

        # Save the database changes.
        self.connection.commit()

    def execute_query(self, query, params=()):
        # Execute a query with the given parameters.
        cursor = self.connection.execute(query, params)

        # Save changes made by the query.
        self.connection.commit()

        # Return the cursor.
        return cursor

    def fetch_all(self, query, params=()):
        # Execute a query and retrieve all matching rows.
        cursor = self.connection.execute(query, params)

        # Return all results as a list of rows.
        return cursor.fetchall()

    def fetch_one(self, query, params=()):
        # Execute a query and retrieve the first matching row.
        cursor = self.connection.execute(query, params)

        # Return one result, or None if no result is found.
        return cursor.fetchone()

    def close(self):
        # Check if the database connection exists.
        if self.connection:
            # Close the database connection.
            self.connection.close()

            # Set the connection to None after closing it.
            self.connection = None
