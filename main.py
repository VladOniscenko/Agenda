from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton, QWidget, QComboBox
from numpy.ma.core import empty

from Controllers.agenda_controller import AgendaController


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.agenda = AgendaController(1)
        self.setWindowTitle("Main Window")
        self.setFixedSize(300, 200)  # Disable resizing by setting a fixed size

        # Button to open "Create Task" window
        self.open_task_window_button = QPushButton("Open Create Task Window")
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
        layout.addWidget(self.description_input)

        # Status input
        self.status_combo = QComboBox()
        self.status_combo.addItems(self.agenda.get_statuses())  # Add options to combo box from TODO_STATUSES tuple
        layout.addWidget(self.status_combo)

        # Submit button
        self.submit_button = QPushButton("Submit")
        self.submit_button.clicked.connect(self.submit_task)
        layout.addWidget(self.submit_button)

        # Set layout
        self.setLayout(layout)
        self.custom_style_sheet()

    def custom_style_sheet(self):
        # submit bg - #1E90FF
        # submit color - black
        # font - white
        # actions / active color - #1E90FF

        self.setStyleSheet('''
            QWidget {
                background-color: white;
                color: black;
                font: 300 13pt "Avenir";
                font-size: 15px;
            }

            QPushButton {
                background-color: #1E90FF;
                border-radius: 5px;
                padding: 7px;
                color: white;
            }

            QPlainTextEdit, QTextEdit, QLineEdit, QComboBox {
                border-radius: 5px;
                border: 1px solid #1E90FF;
                padding: 5px;
            }
        ''')

        # Force refresh
        self.style().polish(self)

    def submit_task(self):
        name = self.name_input.text()
        description = self.description_input.toPlainText()
        selected_status = self.status_combo.currentText()

        # check if inputs are not empty
        if name == '' or description == '' or selected_status == '':
            return

        # create task
        create_response = self.agenda.add_task(name, description, status=selected_status)
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
