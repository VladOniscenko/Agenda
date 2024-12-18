class TaskManager:
    def __init__(self):
        self.__tasks = []

    def __str__(self):
        return 'All tasks:\n' + '\n'.join([f'{'-' * 25}\n{task}' for task in self.__tasks])

    def add_task(self, task):
        self.__tasks.append(task)