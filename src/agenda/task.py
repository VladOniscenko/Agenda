from datetime import datetime, timedelta

class Task:
    def __init__(self, title: str, description: str, due_date: datetime | None = None, status: str = 'pending', priority: int = 1):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.status = status
        self.priority = priority

    def __str__(self):
        return f'Title: {self.title}\nDescription: {self.description}\nDue date: {self.due_date}\nStatus: {self.status}\nPriority: {self.priority}'