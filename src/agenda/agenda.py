from datetime import datetime, timedelta
from .task_manager import TaskManager
from .task import Task

class Agenda:
    def __init__(self):
        self.task_manager = TaskManager()

    def create_task(self, title: str, description: str, due_date: datetime | None = None, status: str = 'pending', priority: int = 1):
        # create a task
        task = Task(title, description, due_date, status, priority)

        # add task to task manager
        self.task_manager.add_task(task)

    def read_task(self):
        pass

    def update_task(self):
        pass

    def delete_task(self):
        pass