from PyQt6.QtCore import QDateTime
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, QTextEdit, QPushButton, QWidget, QTableWidget, QTableWidgetItem, QGridLayout, QComboBox, QDateTimeEdit
from datetime import datetime

from Controllers.agenda_controller import AgendaController
from Models.task import Task


class MainWindow(QMainWindow):
    # todo create header
    # todo on task click open description/update window
    # todo add delete delete button by update page
    # todo checkbox to marks as completed
    # todo after task creation order task by date and then priority

    table_widget: QTableWidget

    def __init__(self):
        self.agenda = AgendaController(1)

        super().__init__()
        self.setWindowTitle("All Tasks")
        self.setFixedSize(400, 550)

        self.container = QWidget()
        self.main_layout = QVBoxLayout()  # Main layout

        # Add the header to the layout
        self.header_layout = QHBoxLayout()
        self.create_header()

        # Add the tasks to the layout
        self.task_list = QVBoxLayout()
        self.create_task_list()

        # Set central widget
        self.container.setLayout(self.main_layout)
        self.setCentralWidget(self.container)

    def create_header(self):
        """Creates the header with today's date and a button to add tasks."""

        # Today's date label
        today_label = QLabel(f"Today: {datetime.now().strftime('%Y-%m-%d')}")
        self.header_layout.addWidget(today_label)

        # Add stretch to push button to the right
        self.header_layout.addStretch()

        # Button to open "Create Task" window
        self.open_task_window_button = QPushButton("+")
        self.open_task_window_button.setFixedSize(30, 30)  # Optional: fix size for aesthetics
        self.open_task_window_button.clicked.connect(self.open_create_task_window)
        self.header_layout.addWidget(self.open_task_window_button)

        self.main_layout.addLayout(self.header_layout)

    def open_create_task_window(self):
        self.task_window = CreateTaskWindow(self)
        self.task_window.show()

    def create_task_list(self):
        # todo create vertical layout
        # todo add tasks to layout



        """Creates and returns the tasks table widget."""
        # self.table_widget = QTableWidget(len(self.agenda.tasks), 4)  # Rows and columns
        # self.table_widget.setHorizontalHeaderLabels(["Name", "Description", "Priority", "Date"])

        # Populate the table
        # self.update_tasks_table(self.table_widget)
        # return self.table_widget

    def update_tasks_table(self, table_widget):
        # todo create label with task name and date
        # todo add prio colors

        """Updates the task table with the latest tasks."""
        # table_widget.setRowCount(len(self.agenda.tasks))  # Update row count
        #
        # for row, task in enumerate(self.agenda.tasks):
        #     table_widget.setItem(row, 0, QTableWidgetItem(task.name))
        #     table_widget.setItem(row, 1, QTableWidgetItem(task.description))
        #     table_widget.setItem(row, 2, QTableWidgetItem(task.priority))
        #     table_widget.setItem(row, 3, QTableWidgetItem(str(task.date)))


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
    app = QApplication([])
    main_window = MainWindow()
    main_window.show()
    app.exec()
