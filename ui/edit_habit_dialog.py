from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLineEdit, QLabel, QPushButton

class EditHabitDialog(QDialog):
    def __init__(self, habit_name, habit_description, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Edit Habit")
        self.setGeometry(200, 200, 400, 200)

        self.layout = QVBoxLayout(self)

        #Input fields for habit name and description
        self.habit_name_input = QLineEdit(self)
        self.habit_name_input.setText(habit_name)
        self.habit_description_input = QLineEdit(self)
        self.habit_description_input.setText(habit_description)

        self.layout.addWidget(QLabel("Habit Name:"))
        self.layout.addWidget(self.habit_name_input)
        self.layout.addWidget(QLabel("Description:"))
        self.layout.addWidget(self.habit_description_input)

        # Ok and Cancel buttons
        self.ok_button = QPushButton("OK", self)
        self.cancel_button = QPushButton("Cancel", self)

        self.layout.addWidget(self.ok_button)
        self.layout.addWidget(self.cancel_button)

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
    
    def get_data(self):
        # Method to retrieve the edited habit name and description
        return self.habit_name_input.text(), self.habit_description_input.text()