import os
import sys
from datetime import datetime

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QScrollArea, QLabel, QMainWindow, QApplication, \
    QHBoxLayout, QDateTimeEdit, QComboBox, QTextEdit, QLineEdit

from Controllers.agenda_controller import AgendaController
from Models.task import Task


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.agenda = AgendaController(1)

        # Create the main widget and layout
        self.main_widget = QWidget()
        self.main_widget.setFixedSize(400, 550)
        self.main_layout = QVBoxLayout(self.main_widget)

        self.create_header()
        self.set_tasks_list()

        # Set the main widget as the central widget of the main window
        self.setCentralWidget(self.main_widget)
        self.show()

    def set_tasks_list(self):
        # Create the scrollable container
        scroll_area = QScrollArea()

        # Create a widget to hold items inside the scrollable container
        scrollable_content = QWidget()
        scrollable_layout = QVBoxLayout(scrollable_content)

        # Add items to the scrollable container
        for num, task in enumerate(self.agenda.tasks):
            # todo add date
            # todo add checkbox
            # todo add prio bg-color

            label = QLabel(f"{task.name}")
            scrollable_layout.addWidget(label)

        # Set the scrollable content inside the scroll area
        scroll_area.setWidget(scrollable_content)

        # Add the scrollable container to the main layout
        self.main_layout.addWidget(scroll_area)

    def create_header(self):
        """Creates the header with today's date and a button to add tasks."""
        task_list = QVBoxLayout()
        header_layout = QHBoxLayout()

        # Today's date label
        today_label = QLabel(f"Today: {datetime.now().strftime('%Y-%m-%d')}")
        header_layout.addWidget(today_label)

        # Add stretch to push button to the right
        header_layout.addStretch()

        # Button to open "Create Task" window
        open_task_window_button = QPushButton("+")
        open_task_window_button.setFixedSize(30, 30)  # Optional: fix size for aesthetics
        open_task_window_button.clicked.connect(self.open_create_task_window)
        header_layout.addWidget(open_task_window_button)

        self.main_layout.addLayout(header_layout)

    def open_create_task_window(self):
        self.task_window = CreateTaskWindow(self)
        self.task_window.show()


class CreateTaskWindow(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.agenda = self.main.agenda

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
        self.status_combo.addItems(Task.statuses())  # Add options to combo box from TODO_STATUSES tuple
        layout.addWidget(self.status_combo)

        # Priority input
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(Task.priorities())  # Add options to combo box from TODO_STATUSES tuple
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
        self.main.update_tasks_table(self.main.table_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()
