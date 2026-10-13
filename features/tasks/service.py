from datetime import date, datetime
from features.tasks.repository import TaskRepository


class TaskService:
    """Handles task business logic, calculations, and validations."""

    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, user_id, title, description, category, priority, due_date, status="Pending"):
        title = title.strip()
        description = description.strip()

        self.validate_task(title, category, priority, due_date, status)
        return self.repository.add(user_id, title, description, category, priority, due_date, status)

    def get_all_tasks(self, user_id):
        return self.repository.get_all(user_id)

    def get_task(self, task_id, user_id):
        return self.repository.get_by_id(task_id, user_id)

    def update_task(self, task_id, user_id, title, description, category, priority, due_date, status):
        title = title.strip()
        description = description.strip()

        self.validate_task(title, category, priority, due_date, status)
        return self.repository.update(task_id, user_id, title, description, category, priority, due_date, status)

    def delete_task(self, task_id, user_id):
        return self.repository.delete(task_id, user_id)

    @staticmethod
    def validate_task(title, category, priority, due_date, status):
        if not title:
            raise ValueError("Task title cannot be empty.")

        if category not in ["School", "Project", "Personal", "Other"]:
            raise ValueError("Please select a valid category.")

        if priority not in ["Low", "Medium", "High"]:
            raise ValueError("Please select a valid priority.")

        if status not in ["Pending", "Completed"]:
            raise ValueError("Please select a valid status.")

        try:
            datetime.strptime(due_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Please enter a valid due date.")

    @staticmethod
    def get_due_state(task):
        if task.status == "Completed":
            return "Completed"

        try:
            due_date = datetime.strptime(task.due_date, "%Y-%m-%d").date()
        except ValueError:
            return "Upcoming"

        days_remaining = (due_date - date.today()).days

        if days_remaining < 0:
            return "Overdue"
        if days_remaining <= 2:
            return "Due Soon"

        return "Upcoming"

    def get_statistics(self, user_id):
        tasks = self.get_all_tasks(user_id)
        return {
            "total": len(tasks),
            "pending": sum(t.status == "Pending" for t in tasks),
            "completed": sum(t.status == "Completed" for t in tasks),
            "overdue": sum(self.get_due_state(t) == "Overdue" for t in tasks),
            "due_soon": sum(self.get_due_state(t) == "Due Soon" for t in tasks),
        }