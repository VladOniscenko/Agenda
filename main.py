import os
import sys
from datetime import datetime
from functools import partial

from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QScrollArea, QLabel, QMainWindow, QApplication, \
    QHBoxLayout, QDateTimeEdit, QComboBox, QTextEdit, QLineEdit, QCheckBox, QSizePolicy

from Controllers.agenda_controller import AgendaController
from Models.task import Task


class MainWindow(QMainWindow):
    scroll_area: QScrollArea

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

        self.create_task_list()

        # # Set the main container/widget as the central widget
        self.setCentralWidget(self.main_widget)

        # show / open our window
        self.show()

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

    def open_task_info(self, event, task: Task):
        print(task)

    def mark_complete(self, event, task: Task):
        print(f"Task marked as complete: {task.id}")

    def create_task_list(self, all = False):
        # Create scrollable area
        self.scroll_area = QScrollArea()
        self.scroll_area.setObjectName('task_list')

        # Create container where content will be placed
        scrollable_content = QWidget()
        scrollable_content.setContentsMargins(0, 0, 0, 0)  # Set margins

        # Set layout to our container
        layout = QVBoxLayout(scrollable_content)
        layout.setContentsMargins(0, 0, 0, 0)  # Set margins
        layout.setSpacing(5)  # Optional: Add spacing between items

        if len(self.agenda.tasks) < 1:
            no_items_label = QLabel('No items found')
            no_items_label.setStyleSheet("""
                color: crimson;
                padding: 20px;
            """)
            layout.addWidget(no_items_label)

        # Add items to the scrollable container layout
        for num, task in enumerate(self.agenda.tasks):
            if not all and task.status in ('Cancelled', 'Completed'):
                continue

            # Create item container
            item_container = QWidget()
            item_container.setObjectName("itemContainer")  # Set a unique object name
            item_container.setFixedHeight(50)

            # get task colors
            item_bg_color, item_text_color = task.status_color

            item_container.setStyleSheet(f"""
                QWidget#itemContainer {{
                    background-color: {item_bg_color};
                    color: {item_text_color};
                }}
                
                QWidget#itemContainer:hover {{
                    background-color: rgba(255, 255, 255, 0.15);
                }}
                
                QCheckBox {{
                    padding-left: 15px;
                    padding-right: 15px;
                }}

                QCheckBox::indicator {{
                    width: 20px;
                    height: 20px;
                    border-radius: 11px;
                    border: 1px solid gray;
                    background-color: rgba(255, 255, 255, 0.1);
                }}

                QCheckBox::indicator:unchecked {{
                    background-color: rgba(255, 255, 255, 0.1);
                }}
            """)

            # Set container layout
            item_layout = QHBoxLayout(item_container)
            item_layout.setContentsMargins(0, 0, 0, 0)  # Remove inner margins

            # Add our item info to layout
            checkbox = QCheckBox()

            item_layout.addWidget(checkbox)

            text = QLabel(f'{task.name}')
            item_layout.addWidget(text)

            # Add stretch to push items to fill space
            item_layout.addStretch()

            # Add the item container to the scrollable layout
            layout.addWidget(item_container)

            # Add event listeners using default argument for task to bind the current task to the lambda
            item_container.mouseReleaseEvent = partial(self.open_task_info, task=task)
            checkbox.mouseReleaseEvent = partial(self.mark_complete, task=task)

        # dont set spaces between items
        layout.addStretch()

        # Add our created content to the scrollable area
        self.scroll_area.setWidget(scrollable_content)
        self.scroll_area.setWidgetResizable(True)  # Ensure the widget resizes with the scroll area

        # Add our scroll area to main content
        self.main_layout.addWidget(self.scroll_area)

    def open_create_task_window(self):
        self.task_window = CreateTaskWindow(self)
        self.task_window.show()

    def update_tasks_list(self):
        self.scroll_area.deleteLater()
        self.create_task_list()

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
        date = self.datetime_input.dateTime().toPython()

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
        self.main.update_tasks_list()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setFixedSize(350, 500)
    window.move(0, 0)

    app.exec()
