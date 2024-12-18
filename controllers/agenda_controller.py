from datetime import datetime
from models.task import Task
from controllers.context_manager import ContextManager

class AgendaController:
    tasks: list
    user_id: int

    def __init__(self):
        self.user_id = 1
        self.tasks = []
        self.db = ContextManager()

    def create_task(self, name: str, description: str, date: datetime = datetime.now(), priority: str = 1, status: str = "Pending") -> Task | bool:
        # create new task in database
        identifier = self.db.execute(
            """
            INSERT INTO tasks (name, description, date, priority, status)
            VALUES (?, ?, ?, ?, ?)
            """,
            (name, description, date, priority, status)
        )

        # if inserted new task
        # create new Task Instance and return it
        if identifier:
            return Task(identifier, name, description, date, priority, status)

        return False

    def read_task(self, task_id):
        pass

    def update_task(self, task_id):
        pass

    def get_task_by_id(self, task_id):
        pass

if __name__ == '__main__':
    agenda = AgendaController()
    agenda.create_task('test', 'test')