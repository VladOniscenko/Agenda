import sys
from asyncio import create_task

from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QTextEdit
from PyQt6.QtCore import Qt
from PyQt6 import uic

from Controllers.agenda_controller import AgendaController


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('Views/create_task.ui', self)
        self.setWindowTitle('Create Task')

        self.agenda = AgendaController(1)

        """
        Create task input fields
        """
        self.create_task_btn.clicked.connect(self.create_task)

    def create_task(self):
        name = self.name.toPlainText()
        description = self.description.toPlainText()

        create_task_response = self.agenda.add_task(name, description)
        if not create_task_response['success']:
            print(create_task_response['message'])
            return

        task = create_task_response['task']
        print(f'Task successfully created! id: {task.id}')

        # todo close creation ui
        # todo open main menu

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('closing window...')