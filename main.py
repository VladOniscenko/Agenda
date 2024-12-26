import os
import sys
from datetime import datetime

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QScrollArea, QLabel, QMainWindow, QApplication, \
    QHBoxLayout, QDateTimeEdit, QComboBox, QTextEdit, QLineEdit, QCheckBox

from Controllers.agenda_controller import AgendaController
from Models.task import Task


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Task Manager")
        self.agenda = AgendaController(1)

        # creating main container main_widget
        self.main_widget = QWidget()

        # add styling to our main widget
        self.main_widget.setStyleSheet("""
        """)

        # create main layout positioning (vertical alignment)
        # add our main widget to our layout
        self.main_layout = QVBoxLayout(self.main_widget)

        # create header and add to our layout
        self.create_header()

        # # Set the main container/widget as the central widget
        self.setCentralWidget(self.main_widget)

        # show / open our window
        self.show()

    def set_tasks_list(self):
        # Create the scrollable container
        scroll_area = QScrollArea()

        # # Create a widget to hold items inside the scrollable container
        scrollable_content = QWidget()
        scrollable_layout = QVBoxLayout(scrollable_content)
        scrollable_layout.setContentsMargins(0, 0, 0, 0)

        # Add items to the scrollable container
        for num, task in enumerate(self.agenda.tasks):
            # todo add date
            # todo add checkbox
            # todo add prio bg-color

            container = QWidget()
            container.setStyleSheet("background-color: green; height: 50px;")
            layout = QHBoxLayout(container)
            checkbox = QCheckBox(f"{task.name}", self)
            layout.addWidget(checkbox)
            scrollable_layout.addWidget(container)

        # Set the scrollable content inside the scroll area
        scroll_area.setWidget(scrollable_content)

        # Add the scrollable container to the main layout
        self.main_layout.addWidget(scroll_area)

    def create_header(self):
        # create header layout type (horizontal layout)
        layout = QHBoxLayout()

        # create a label with text inside
        current_date_label = QLabel(f'Today: {datetime.now().strftime('%Y-%m-%d')}')

        # add our label with text to our layout
        layout.addWidget(current_date_label)

        # take all extra space for next widgets
        layout.addStretch()

        # Button to open "Create Task" window
        create_task_btn = QPushButton("+")  # create button with + as text
        create_task_btn.setFixedSize(30, 30)  # set button size
        create_task_btn.clicked.connect(self.open_create_task_window)  # set event function

        # add button to header layout
        layout.addWidget(create_task_btn)

        # add our created header layout to main layout
        self.main_layout.addLayout(layout)


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
    window.setFixedSize(400, 550)
    window.move(0, 0)

    app.exec()
