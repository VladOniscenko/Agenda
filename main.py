import sys

from functools import partial
from PySide6.QtCore import Qt
from PySide6.QtCore import QDateTime
from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QScrollArea, QLabel, QMainWindow, QApplication, \
    QHBoxLayout, QDateTimeEdit, QComboBox, QTextEdit, QLineEdit, QCheckBox

from Controllers.agenda_controller import AgendaController
from Models.task import Task

WIDTH, HEIGHT = 300, 400
MAIN_BG_COLOR = '#1f1f1f'
SECOND_BG_COLOR = '#2a2a2a'
FALSE_BG_COLOR = 'rgba(77, 46, 46, 0.8)'
FALSE_TEXT_COLOR = 'lightcoral'

class CreateTaskWindow(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.agenda = self.main.agenda

        self.setWindowTitle("Create Task")
        self.setFixedWidth(WIDTH)
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
        if name == '' or selected_status == '' or selected_priority == '' or date == '':
            return

        # create task
        create_response = self.agenda.add_task(name, description, date, selected_priority, selected_status)
        if not create_response['success']:
            print(create_response['message'])
            return

        task = create_response['task']
        print(f"Task created! id: {task.id}")
        self.close()

        self.main.tasks.append(task)
        self.main.update_tasks_list()


class MainWindow(QMainWindow):
    scroll_area: QScrollArea
    calendar: None | QDateTimeEdit
    show_hidden_tasks: QCheckBox
    show_all: QCheckBox
    task_window: CreateTaskWindow

    extended_widget: QWidget
    extended_layout: QVBoxLayout

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Todo's Manager")
        self.agenda = AgendaController(1)

        self.date = QDateTime.currentDateTime()
        self.tasks = []

        # creating main container main_widget
        self.main_widget = QWidget()
        self.main_widget.setObjectName('main_widget')
        self.main_widget.setFixedSize(300, 400)

        # add styling to our main widget
        self.main_widget.setStyleSheet(f"""
            QWidget#main_widget {{
                background-color: {MAIN_BG_COLOR};
            }}
        """)

        # create main layout positioning (vertical alignment)
        self.main_layout = QVBoxLayout(self.main_widget)

        # create header and add to our layout
        self.create_header()
        self.create_task_list()

        # Create the parent horizontal layout
        self.parent_layout_widget = QWidget()
        self.horizontal_layout = QHBoxLayout(self.parent_layout_widget)
        self.horizontal_layout.setSpacing(0)
        self.horizontal_layout.setContentsMargins(0,0,0,0)

        # Add main_widget to the horizontal layout
        self.horizontal_layout.addWidget(self.main_widget)

        # Set the parent layout widget as the central widget
        self.setCentralWidget(self.parent_layout_widget)

        # show / open our window
        self.show()

    def create_header(self):
        # create header layout type (horizontal layout)
        layout = QHBoxLayout()

        # calendar select box
        self.calendar = QDateTimeEdit(self.date)
        self.calendar.setDisplayFormat("dd-MM-yyyy")
        self.calendar.setCalendarPopup(True)
        self.calendar.dateChanged.connect(self.change_date)

        self.show_hidden_tasks = QCheckBox('Show processed')
        self.show_hidden_tasks.clicked.connect(self.update_tasks_list)

        self.show_all = QCheckBox('Show all dates')
        self.show_all.setVisible(False)
        self.show_all.clicked.connect(self.update_tasks_list)

        # Create a vertical layout for checkboxes
        checkbox_layout = QVBoxLayout()
        checkbox_layout.addWidget(self.show_hidden_tasks)
        checkbox_layout.addWidget(self.show_all)

        # add our calendar to our layout
        layout.addWidget(self.calendar)
        layout.addLayout(checkbox_layout)

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

    def open_task_info(self, _, task: Task):
        item_bg_color, item_text_color = task.status_color
        widget, layout = self.create_extended_tab()

        # Construct head of info widget
        head = QWidget()
        head_layout = QHBoxLayout(head)
        head_layout.setContentsMargins(0, 0, 0, 0)

        # create task head layout with status and close button
        task_status = QLabel(f'Task {task.status}')
        task_status.setStyleSheet(f"""
            background-color: {item_bg_color};
            color: {item_text_color};
            text-transform: uppercase;
            font-weight: bold;
            padding: 10px;
            border: solid 1px {item_text_color};
            border-radius: 5px;
        """)

        head_layout.addWidget(task_status)

        # add priority to head
        item_bg_color, item_text_color = task.priority_color
        task_priority = QLabel(f'{task.priority} Priority')
        task_priority.setStyleSheet(f"""
            background-color: {item_bg_color};
            color: {item_text_color};
            text-transform: uppercase;
            font-weight: bold;
            padding: 10px;
            border: solid 1px {item_text_color};
            border-radius: 5px;
        """)
        head_layout.addWidget(task_priority)

        # stretch head for close button
        head_layout.addStretch()

        close = QPushButton(f'X')
        close.clicked.connect(self.close_extended_tab)
        close.setStyleSheet(f"background-color: {FALSE_BG_COLOR}; color: {FALSE_TEXT_COLOR};")

        head_layout.addWidget(close)
        layout.addWidget(head)

        # create task name
        task_name = QLabel(f'{task.name}')
        task_name.setStyleSheet(f"""
            font-size: 20px;
            font-weight: bold;
            border: solid 1px pink;
        """)
        task_name.setWordWrap(True)
        layout.addWidget(task_name)

        # create task description
        task_name = QLabel(f'{task.description}')
        task_name.setStyleSheet("""
        """)
        task_name.setWordWrap(True)
        layout.addWidget(task_name)

        self.setFixedWidth(int(WIDTH * 2.5))
        self.horizontal_layout.addWidget(widget)

        print(task)

    def mark_complete(self, _, task: Task):
        update = self.agenda.set_as_completed(task.id)
        if update['success']:
            print(f"Task marked as complete: {task.id}")
            self.update_tasks_list()
        else:
            print(f"{update['message']}")

    def create_task_list(self):
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

        # showed tasks count
        showed_tasks_count = 0

        if self.show_all.isChecked():
            get_tasks_response = self.agenda.get_tasks()
        else:
            get_tasks_response = self.agenda.get_tasks(self.date.toString('yyyy-MM-dd'))

        self.tasks = get_tasks_response['tasks'] if get_tasks_response['success'] else []

        # Add items to the scrollable container layout
        for num, task in enumerate(self.tasks):
            if not self.show_hidden_tasks.isChecked() and task.status in ('Cancelled', 'Completed'):
                continue

            showed_tasks_count += 1

            # Create item container
            item_container = QWidget()
            item_container.setObjectName("itemContainer")  # Set a unique object name
            item_container.setContentsMargins(15, 0, 15, 0)
            item_container.setFixedHeight(50)

            # get task colors
            item_bg_color, item_text_color = task.priority_color
            if task.status == 'Completed':
                item_bg_color, _ = task.status_color

            item_container.setStyleSheet(f"""
                QWidget#itemContainer {{
                    background-color: {item_bg_color};
                    color: {item_text_color};
                }}
                
                QWidget#itemContainer:hover {{
                    background-color: rgba(255, 255, 255, 0.15);
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
                
                QCheckBox::indicator:hover {{
                    background-color: rgba(46, 77, 46, 0.8);
                }}
            """)

            # Set container layout
            item_layout = QHBoxLayout(item_container)
            item_layout.setContentsMargins(0, 0, 0, 0)  # Remove inner margins

            if task.status != 'Completed':
                # Add our item info to layout
                checkbox = QCheckBox()
                item_layout.addWidget(checkbox)
                checkbox.mouseReleaseEvent = partial(self.mark_complete, task=task)

            task_name = task.name
            if len(task.name) > 25:
                task_name = task.name[:25] + '...'

            text = QLabel(f'{task_name}')
            text.setStyleSheet(f"color: {item_text_color};")
            item_layout.addWidget(text)

            # Add stretch to push items to fill space
            item_layout.addStretch()

            time_label = QLabel(task.task_time_label)
            time_label.setObjectName('task_time_label')
            time_label.setStyleSheet(f"""
                QLabel#task_time_label {{
                    color: {item_text_color};
                }}
            """)

            item_layout.addWidget(time_label)

            # Add the item container to the scrollable layout
            layout.addWidget(item_container)

            # Add event listeners
            item_container.mouseReleaseEvent = partial(self.open_task_info, task=task)

        if showed_tasks_count == 0:
            no_items_label = QLabel('No items found')
            no_items_label.setStyleSheet("""
                color: crimson;
                padding: 20px;
            """)
            layout.addWidget(no_items_label)

        # dont set spaces between items
        layout.addStretch()

        # Add our created content to the scrollable area
        self.scroll_area.setWidget(scrollable_content)
        self.scroll_area.setWidgetResizable(True)  # Ensure the widget resizes with the scroll area

        # Add our scroll area to main content
        self.main_layout.addWidget(self.scroll_area)

    def open_create_task_window(self):
        widget, layout = self.create_extended_tab()

        head = QLabel('Create new task')
        layout.addWidget(head)

        # self.task_window = CreateTaskWindow(self)
        # self.task_window.show()

    def update_tasks_list(self):
        self.scroll_area.deleteLater()
        self.create_task_list()

    def change_date(self, new_date):
        # Handle the selected date
        print(f"Selected date: {new_date.toString('dd-MM-yyyy')}")

        self.date = new_date
        self.update_tasks_list()

    def create_extended_tab(self):
        # check if it is created
        try:
            if hasattr(self, 'extended_widget') and self.extended_widget and self.extended_widget.isWidgetType():
                self.extended_widget.deleteLater()
        except RuntimeError:
            # Handle the case when the widget has already been deleted
            pass

        # Add a layout for the extended_widget
        self.extended_widget = QWidget()
        self.extended_layout = QVBoxLayout(self.extended_widget)
        self.extended_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.extended_widget.setVisible(False)
        self.extended_widget.setObjectName("createWidget")

        self.extended_widget.setStyleSheet(f"""
            QWidget#createWidget {{
                background-color: {SECOND_BG_COLOR};
            }}
        """)

        self.setFixedWidth(int(WIDTH * 2.5))
        self.horizontal_layout.addWidget(self.extended_widget)
        self.extended_widget.setVisible(True)

        return self.extended_widget, self.extended_layout

    def close_extended_tab(self):
        try:
            if hasattr(self, 'extended_widget') and self.extended_widget is not None:
                self.extended_widget.deleteLater()
        except RuntimeError:
            # Handle the case when the widget has already been deleted
            pass
        self.setFixedWidth(WIDTH)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.setFixedSize(WIDTH, HEIGHT)
    window.move(0, 0)

    app.exec()
