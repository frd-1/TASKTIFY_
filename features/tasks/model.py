from dataclasses import dataclass


@dataclass
class Task:
    """Represents a Task entity."""

    id: int
    user_id: int
    title: str
    description: str
    category: str
    priority: str
    due_date: str
    status: str

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            user_id=row["user_id"],
            title=row["title"],
            description=row["description"] or "",
            category=row["category"],
            priority=row["priority"],
            due_date=row["due_date"],
            status=row["status"],
        )