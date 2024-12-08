from datetime import datetime, timedelta

class Task:
    title: str
    description: str
    due_date: datetime
    status: str
    priority: int

    def __init__(self, title: str, description: str, due_date: datetime = datetime.now() + timedelta(hours=1), status: str = 'not_started', priority: int = 1):

        self._statuses = {
            "not_started": "Not Started",
            "in_progress": "In Progress",
            "completed": "Completed",
            "on_hold": "On Hold",
            "cancelled": "Cancelled",
            "overdue": "Overdue",
            "blocked": "Blocked",
            "awaiting_review": "Awaiting Review",
            "deferred": "Deferred",
            "critical": "Critical",
            "in_review": "In Review",
            "planned": "Planned"
        }

        if status not in self._statuses:
            raise ValueError(f"Invalid status: {status}. Valid statuses are: {list(self._statuses.keys())}")

        self.status = self._statuses.get(status, "not_started")
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status
        self.priority = priority

    def __str__(self):
        return f'Title: {self.title}\nDescription: {self.description}\nDue date: {self.due_date}\nStatus: {self.status}\nPriority: {self.priority}'