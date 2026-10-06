from dataclasses import dataclass


@dataclass
class Task:
    """Represents a Task entity."""

    id: int
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
            title=row["title"],
            description=row["description"] or "",
            category=row["category"],
            priority=row["priority"],
            due_date=row["due_date"],
            status=row["status"],
        )