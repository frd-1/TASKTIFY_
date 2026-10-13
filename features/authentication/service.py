import hashlib
from features.authentication.repository import AuthRepository


class AuthService:
    """Business logic service for login and registration."""

    def __init__(self, repository: AuthRepository):
        self.repository = repository

    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()

    def register(self, username: str, password: str):
        username = username.strip()
        password = password.strip()

        if not username or not password:
            return False, "Username and password cannot be empty."

        if self.repository.get_by_username(username):
            return False, "Username already exists."

        pwd_hash = self._hash_password(password)
        self.repository.create_user(username, pwd_hash)
        return True, "Registration successful! You can now log in."

    def login(self, username: str, password: str):
        username = username.strip()
        password = password.strip()

        user = self.repository.get_by_username(username)
        if not user:
            return False, "User does not exist.", None

        if user["password_hash"] == self._hash_password(password):
            return True, "Login successful!", user

        return False, "Invalid password.", None