from datetime import datetime, timedelta
from Models.task import Task
from Controllers.context_manager import ContextManager


class AgendaController:
    tasks: list
    user_id: int
    user_id: int
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.db = ContextManager()


    def add_task(self, name: str, description: str, date: datetime = datetime.now(), priority: str = 1, status: str = "Pending") -> Task | dict:
        # create new task in database
        identifier = self.db.execute(
            """
            INSERT INTO tasks (name, description, date, priority, status, user_id)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, description, date, priority, status, self.user_id)
        )

        if not identifier:
            # return false if task was not created
            return {
                'success': False,
                'message': 'Something went wrong! Task could\'t be created'
            }

        # create new Task Instance and return it
        return {
            'success': True,
            'task': Task(name, description, date, priority, status, identifier=identifier)
        }

    def get_task(self, task_id):
        # search for task in database
        raw_task = self.db.execute(
            "SELECT name, description, date, priority, status, id FROM tasks WHERE id = ? and user_id = ?",
            (task_id, self.user_id),
            fetch_mode = 'one'
        )

        # check if task was found
        if not raw_task:
            return {
                'success': False,
                'message': f'Task with id:{task_id} was not found!'
            }

        # create Task instance and return it
        return {
            'success': True,
            'task': Task(*raw_task[:5], identifier=raw_task[5])
        }

    def get_tasks(self, date: str|None = None) -> dict:
        # Base query
        query = """
            SELECT name, description, date, priority, status, id
            FROM tasks
            WHERE user_id = ?
        """
        params = [self.user_id]

        # Add condition for filtering by date if 'date' is provided
        if date:
            # Convert the input date from 'd-m-Y' format to 'YYYY-MM-DD'
            formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
            query += " AND DATE(date) = ?"
            params.append(formatted_date)

        # Append sorting logic
        query += """
            ORDER BY CASE priority
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Medium' THEN 3
                WHEN 'Low' THEN 4
                ELSE 5
            END;
        """

        # search for tasks in database
        raw_tasks = self.db.execute(query, params)

        # check if tasks were found
        if not raw_tasks:
            return {
                'success': False,
                'message': 'Something went wrong!'
            }

        # create Task instances and return them
        return {
            'success': True,
            'tasks': [Task(*raw_task[:5], identifier=raw_task[5]) for raw_task in raw_tasks]
        }

    def update_task(self, task_id: int, name: str, description: str, date: datetime, priority: str, status: str):
        # Update task in the database
        result = self.db.execute(
            """
            UPDATE tasks
            SET name = ?, description = ?, date = ?, priority = ?, status = ?
            WHERE id = ? AND user_id = ?
            """,
            (name, description, date, priority, status, task_id, self.user_id)
        )

        if not result:
            # Return false if the task was not updated
            return {
                'success': False,
                'message': 'Something went wrong! Task could not be updated'
            }

        # Return success with the updated Task instance
        return {
            'success': True,
            'task': Task(name, description, date, priority, status, identifier=task_id)
        }

    def delete_task(self, task_id: int):
        # delete task from database
        deleted = self.db.execute(
            'DELETE FROM tasks WHERE id = ?',
            (task_id, )
        )

        # check if deleted
        if deleted:
            return {
                'success': True,
            }

        return {
            'success': False,
            'message': 'Something went wrong!'
        }

    def set_as_completed(self, identifier: int) -> dict:
        update = self.db.execute(
            """
                UPDATE tasks
                SET status = 'Completed'
                WHERE id = ?
            """,
            (identifier, )
        )

        # check if updated
        if update:
            return {
                'success': True,
            }

        return {
            'success': False,
            'message': 'Something went wrong!'
        }