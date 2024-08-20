import sqlite3  # Import the SQLite library to manage the database operations
from PyQt6.QtWidgets import QMessageBox

class Database:
    def __init__(self, db_name="habits.db"):
        self.connection = sqlite3.connect(db_name)  # Connect to the database specified by db_name
        self.cursor = self.connection.cursor()  # Create a cursor object to execute SQL commands
        self.create_table()  # Create the 'habits' table if it doesn't exist
        self.create_habit_progress_table()  # Create the 'habit_progress' table if it doesn't exist

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT NOT NULL
            )
        ''')
        self.connection.commit()  # Save (commit) the changes to the database
    
    def create_habit_progress_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER,
                date TEXT NOT NULL,
                status INTEGER NOT NULL,
                FOREIGN KEY(habit_id) REFERENCES habits(id),
                UNIQUE(habit_id, date)  -- This ensures that each habit_id and date combination is unique
            )
        ''')
        self.connection.commit()


    
    def add_habit(self, name, description):
        # Insert a new habit into the database
        self.cursor.execute('''
            INSERT INTO habits (name, description)
            VALUES (?, ?)
        ''', (name, description))
        self.connection.commit()

    
    def get_habits(self):
        self.cursor.execute('SELECT name, description FROM habits')
        return self.cursor.fetchall()  # Return the results as a list of tuples

    def delete_habit(self, name, description):
        self.cursor.execute('''
            DELETE FROM habits WHERE name = ? AND description = ?
        ''', (name, description))  # Use placeholders to securely identify the habit to delete
        self.connection.commit()  # Save (commit) the changes to the database

    def save_progress(self, habit_id, date, status):
        self.cursor.execute('''
            INSERT INTO habit_progress (habit_id, date, status)
            VALUES (?, ?, ?)
            ON CONFLICT(habit_id, date)
            DO UPDATE SET status = excluded.status
        ''', (habit_id, date, status))
        self.connection.commit()
    
    def get_progress(self, habit_id, start_date, end_date):
        self.cursor.execute('''
            SELECT date, status FROM habit_progress
            WHERE habit_id = ? AND date BETWEEN ? AND ?
        ''', (habit_id, start_date, end_date))  # Use placeholders to securely query progress data
        return self.cursor.fetchall()  # Return the results as a list of tuples

    def get_habit_id(self, name, description):
        self.cursor.execute('''
            SELECT id FROM habits WHERE name = ? AND description = ?
        ''', (name, description))  # Use placeholders to securely query the habit's ID

        result = self.cursor.fetchone() # Fetch the first result
        if result: # Check if a result was found
            return result[0] # Return the habit ID
        else:
            # Showing a dialog box informing that the habit was not found
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Warning)
            msg_box.setText(f"Habit '{name}' with description '{description}' not found in the database.")
            msg_box.setWindowTitle("Habit Deleted")
            msg_box.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg_box.exec() # Display the dialog box
            return None # Return None to indicate no ID was found

    def close(self):
        self.connection.close()  # Safely close the database connection