from dataclasses import dataclass


@dataclass
class User:
    """Represents a User entity."""

    id: int
    username: str
    password_hash: str