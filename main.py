from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QWidget, QComboBox, QDateTimeEdit

from Controllers.agenda_controller import AgendaController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.agenda = AgendaController(1)
        self.setWindowTitle("All tasks")
        self.setFixedWidth(300)

        # Button to open "Create Task" window
        self.open_task_window_button = QPushButton("+")
        self.open_task_window_button.clicked.connect(self.open_create_task_window)

        # Set layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.open_task_window_button)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def open_create_task_window(self):
        self.task_window = CreateTaskWindow(self.agenda)
        self.task_window.show()


class CreateTaskWindow(QWidget):
    def __init__(self, agenda):
        super().__init__()
        self.agenda = agenda

        self.setWindowTitle("Create Task")
        self.setFixedWidth(300)
        self.adjustSize()

        # Layout and widgets
        layout = QVBoxLayout()

        # Name input
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name...")
        layout.addWidget(self.name_input)

        # Description input
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Description...")
        self.description_input.setFixedHeight(100)
        layout.addWidget(self.description_input)

        # Status input
        self.status_combo = QComboBox()
        self.status_combo.addItems(self.agenda.get_statuses())  # Add options to combo box from TODO_STATUSES tuple
        layout.addWidget(self.status_combo)

        # Priority input
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(self.agenda.get_priorities())  # Add options to combo box from TODO_STATUSES tuple
        layout.addWidget(self.priority_combo)

        # Datetime input
        self.datetime_input = QDateTimeEdit()
        self.datetime_input.setDateTime(QDateTime.currentDateTime().addSecs(3600))  # Set initial value to 1 hour ahead
        self.datetime_input.setCalendarPopup(True)  # Enable the calendar popup
        layout.addWidget(self.datetime_input)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_task)
        layout.addWidget(self.submit_button)

        # Set layout
        self.setLayout(layout)

    def submit_task(self):
        name = self.name_input.text()
        description = self.description_input.toPlainText()
        selected_status = self.status_combo.currentText()
        selected_priority = self.priority_combo.currentText()
        date = self.datetime_input.dateTime().toPyDateTime()

        # check if inputs are not empty
        if name == '' or description == '' or selected_status == '' or selected_priority == '' or date == '':
            return

        # create task
        create_response = self.agenda.add_task(name, description, date, selected_priority, selected_status)
        if not create_response['success']:
            print(create_response['message'])
            return

        task = create_response['task']
        print(f"Task created! id: {task.id}")
        self.close()


if __name__ == '__main__':
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
