# HabitTracker/ui/statistics_widget.py

import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QVBoxLayout, QWidget, QComboBox, QLabel
from PyQt6.QtCore import QDate, Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from database import Database

class StatisticsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.habit_selector = QComboBox(self)
        self.habit_selector.currentIndexChanged.connect(self.plot_progress)
        self.layout.addWidget(QLabel("Select a habit: "))
        self.layout.addWidget(self.habit_selector)
        self.figure = plt.figure(facecolor='darkblue')
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)
        self.database = Database()
        self.load_habits()
        self.plot_progress()

    def load_habits(self):
        habits = self.database.get_habits()
        for habit in habits:
            self.habit_selector.addItem(f"{habit[0]}: {habit[1]}")

    def plot_progress(self):
        self.figure.clear()
        
        selected_habit = self.habit_selector.currentText()
        if not selected_habit:
            return

        habit_name, habit_description = selected_habit.split(": ", 1)
        habit_id = self.database.get_habit_id(habit_name, habit_description)

        end_date = QDate.currentDate().toString(Qt.DateFormat.ISODate)
        start_date = QDate.currentDate().addDays(-6).toString(Qt.DateFormat.ISODate)


        data = self.get_data(habit_id, start_date, end_date)
        ax = self.figure.add_subplot(111)
        ax.set_facecolor('#2b2b2b')  # Set the background color to dark grey
        ax.plot(data['dates'], data['streaks'], color='white')  # Use a single color string
        self.canvas.draw()

    def get_data(self, habit_id, start_date, end_date):
        progress_data = self.database.get_progress(habit_id, start_date, end_date)

        dates = [entry[0] for entry in progress_data]
        streaks = [entry[1] for entry in progress_data]

        return {
            'dates': dates,
            'streaks': streaks
        }