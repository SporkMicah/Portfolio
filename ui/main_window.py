from PyQt6.QtWidgets import (
    QMainWindow, QMenuBar, QStatusBar, QVBoxLayout, QWidget, QLabel,
    QFormLayout, QLineEdit, QPushButton, QListWidget, QMenu, QMessageBox, QCheckBox, QGridLayout, QDialog
)
from PyQt6.QtCore import Qt, QPoint, QDate
from database import Database
from ui.statistics_widget import StatisticsWidget  # Import the StatisticsWidget
from ui.edit_habit_dialog import EditHabitDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()  # Initialize the base QMainWindow class

        self.setWindowTitle("Habit Tracker")  # Set the window title
        self.setGeometry(100, 100, 800, 600)  # Set the size and position of the window

        # Initialize the database connection
        self.database = Database()

        # Menu Bar
        self.menu_bar = QMenuBar(self)  # Create a menu bar
        self.setMenuBar(self.menu_bar)  # Set the menu bar in the main window

        # Status Bar
        self.status_bar = QStatusBar(self)  # Create a status bar
        self.setStatusBar(self.status_bar)  # Set the status bar in the main window

        # Central Widget
        self.central_widget = QWidget(self)  # Create a central widget
        self.setCentralWidget(self.central_widget)  # Set the central widget in the main window

        # Layout for the Central Widget
        self.layout = QVBoxLayout(self.central_widget)  # Create a vertical box layout for the central widget

        # Form for Adding a New Habit
        self.form_layout = QFormLayout()  # Create a form layout for input fields

        self.habit_name_input = QLineEdit(self)  # Create an input field for habit name
        self.habit_description_input = QLineEdit(self)  # Create an input field for habit description
        self.add_habit_button = QPushButton("Add Habit", self)  # Create a button to add a habit
        self.add_habit_button.clicked.connect(self.add_habit)  # Connect the button click to the add_habit method

        self.form_layout.addRow("Habit Name: ", self.habit_name_input)  # Add the habit name input field to the form layout
        self.form_layout.addRow("Description: ", self.habit_description_input)  # Add the habit description input field to the form layout
        self.form_layout.addWidget(self.add_habit_button)  # Add the "Add Habit" button to the form layout

        # Adding the form layout to the main layout
        self.layout.addLayout(self.form_layout)  # Add the form layout to the central widget's layout

        # List Widget to Display Habits
        self.habit_list = QListWidget(self)  # Create a list widget to display the list of habits
        self.habit_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)  # Enable custom context menus on the list
        self.habit_list.customContextMenuRequested.connect(self.show_context_menu)  # Connect right-click to show_context_menu
        self.habit_list.itemSelectionChanged.connect(self.display_progress)  # Update progress display when a habit is selected
        self.layout.addWidget(self.habit_list)  # Add the list widget to the main layout

        # Daily Checkboxes for Habit Tracking
        self.daily_checkboxes = {}  # Dictionary to hold daily checkboxes for tracking progress
        self.grid_layout = QGridLayout()  # Create a grid layout for the checkboxes
        for day in range(7):  # Loop over the days of the week
            checkbox = QCheckBox(f"Day {day + 1}")  # Create a checkbox for each day
            self.daily_checkboxes[day] = checkbox  # Store the checkbox in the dictionary
            self.grid_layout.addWidget(checkbox, 0, day)  # Place each checkbox in the grid layout
        self.layout.addLayout(self.grid_layout)  # Add the grid layout to the main layout

        for day, checkbox in self.daily_checkboxes.items():
            checkbox.stateChanged.connect(lambda state, day=day: self.update_progress(day, state))  # Connect checkbox state changes to update_progress

        # Statistics Widget for Data Visualization
        self.statistics_widget = StatisticsWidget(self)  # Create an instance of the StatisticsWidget
        self.layout.addWidget(self.statistics_widget)  # Add the statistics widget to the main layout

        # Load habits into the list
        self.load_habits()  # Load and display habits in the list widget

        # Set the layout
        self.central_widget.setLayout(self.layout)  # Set the main layout for the central widget

    def add_habit(self):
        # Method to add a new habit to the database
        habit_name = self.habit_name_input.text()  # Get the text from the habit name input field
        habit_description = self.habit_description_input.text()  # Get the text from the habit description input field

        if habit_name and habit_description:  # Check if both fields are not empty
            self.database.add_habit(habit_name, habit_description)  # Add the habit to the database
            self.habit_name_input.clear()  # Clear the habit name input field
            self.habit_description_input.clear()  # Clear the habit description input field
            self.load_habits()  # Reload the list of habits to include the new habit
            print(f"New Habit Added: {habit_name} - {habit_description}")  # Print confirmation to the console
        else:
            print("Please enter both the habit name and description.")  # Print error message if fields are empty

    def load_habits(self):
        # Method to load habits from the database and display them in the list widget
        self.habit_list.clear()  # Clear the list widget before loading new items
        habits = self.database.get_habits()  # Retrieve the list of habits from the database
        for habit in habits:  # Iterate over each habit
            self.habit_list.addItem(f"{habit[0]}: {habit[1]}")  # Add the habit to the list widget

    def display_progress(self):
        selected_item = self.habit_list.currentItem()  # Get the currently selected habit from the list
        if selected_item:  # Check if an item is selected
            habit_name, habit_description = selected_item.text().split(": ", 1)  # Split the selected text into name and description
            habit_id = self.database.get_habit_id(habit_name, habit_description)  # Get the habit ID from the database
            
            if habit_id is None:  # If no habit ID was found, return early
                return
            
            start_date = QDate.currentDate().addDays(-6).toString(Qt.DateFormat.ISODate)  # Calculate the start date (7 days ago)
            end_date = QDate.currentDate().toString(Qt.DateFormat.ISODate)  # Get today's date as the end date
            progress = self.database.get_progress(habit_id, start_date, end_date)  # Get progress data from the database
            for day, checkbox in self.daily_checkboxes.items():  # Iterate over each checkbox
                date = QDate.currentDate().addDays(-day).toString(Qt.DateFormat.ISODate)  # Calculate the date for each checkbox
                checkbox.setChecked(any(date == p[0] and p[1] == 1 for p in progress))  # Check or uncheck the checkbox based on progress


    def show_context_menu(self, position: QPoint):
        # Method to display the context menu for editing or deleting habits
        context_menu = QMenu(self)  # Create a context menu
        delete_action = context_menu.addAction("Delete Habit")  # Add a delete action to the menu
        edit_action = context_menu.addAction("Edit Habit")  # Add an edit action to the menu
        action = context_menu.exec(self.habit_list.mapToGlobal(position))  # Show the context menu at the cursor position
        
        if action == delete_action:  # If delete action is selected
            self.delete_habit()  # Call the delete_habit method
        elif action == edit_action:  # If edit action is selected
            self.edit_habit()  # Call the edit_habit method

    def delete_habit(self):
        # Method to delete the selected habit
        selected_item = self.habit_list.currentItem()  # Get the currently selected habit from the list
        if selected_item:  # Check if an item is selected
            habit_name, habit_description = selected_item.text().split(": ", 1)  # Split the selected text into name and description
            reply = QMessageBox.question(
                self, "Delete Habit",
                f"Are you sure you want to delete the habit '{habit_name}'?",  # Show a confirmation dialog
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:  # If the user confirms deletion
                self.database.delete_habit(habit_name, habit_description)  # Delete the habit from the database
                self.load_habits()  # Reload the list of habits
                print(f"Habit Deleted: {habit_name} - {habit_description}")  # Print confirmation to the console

    def edit_habit(self):
        # Method to edit the selected habit
        selected_item = self.habit_list.currentItem()  # Get the currently selected habit from the list
        if selected_item:  # Check if an item is selected
            habit_name, habit_description = selected_item.text().split(": ", 1)  # Split the selected text into name and description
            dialog = EditHabitDialog(habit_name, habit_description)  # Create an edit habit dialog with the current habit data
            if dialog.exec() == QDialog.DialogCode.Accepted:  # If the user confirms the edit
                new_name, new_description = dialog.get_data()  # Get the new habit data from the dialog
                self.database.delete_habit(habit_name, habit_description)  # Delete the old habit from the database
                self.database.add_habit(new_name, new_description)  # Add the edited habit to the database
                self.load_habits()  # Reload the list of habits
                print(f"Habit Edited: {new_name} - {new_description}")  # Print confirmation to the console

    def update_progress(self, day, state):
        # Method to update the progress of the selected habit for a specific day
        selected_item = self.habit_list.currentItem()  # Get the currently selected habit from the list
        if selected_item:  # Check if an item is selected
            habit_name, habit_description = selected_item.text().split(": ", 1)  # Split the selected text into name and description
            habit_id = self.database.get_habit_id(habit_name, habit_description)  # Get the habit ID from the database
            date = QDate.currentDate().addDays(-day).toString(Qt.DateFormat.ISODate)  # Calculate the date for the checkbox
            status = 1 if state == Qt.CheckState.Checked else 0  # Determine the status based on checkbox state
            self.database.save_progress(habit_id, date, status)  # Save the progress in the database
            print(f"Progress saved for {habit_name} on {date} with status {status}")  # Print confirmation to the console
