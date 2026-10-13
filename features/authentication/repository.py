from database.database import Database


class AuthRepository:
    """Handles database queries for user authentication."""

    def __init__(self, db: Database):
        self.db = db

    def create_user(self, username, password_hash):
        cursor = self.db.execute_query("""
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        """, (username, password_hash))
        return cursor.lastrowid

    def get_by_username(self, username):
        row = self.db.fetch_one("""
            SELECT id, username, password_hash FROM users WHERE username = ?
        """, (username,))
        return dict(row) if row else None