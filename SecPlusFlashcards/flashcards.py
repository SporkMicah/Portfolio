import tkinter as tk
from random import shuffle

#Function to load acronyms from a file
def load_acronyms(filename):
    acronyms_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2: #Ensure the line has exactly two parts
                acronyms_dict[parts[0]] = parts[1]
    return acronyms_dict

# Load acronyms from the file
acronyms = load_acronyms('acronyms.txt')

# Create a list of tuples from the dictionary
acronym_list = list(acronyms.items())
shuffle(acronym_list) # Shuffle the list to randomize flashcards

# Create the main applications window
app = tk.Tk()
app.title("CompTIA Security+ Acronym Flashcards")

# Initialize variables
current_acronym = tk.StringVar()
current_meaning = tk.StringVar()
index = [0] # Use a list to maintain reference in nested functions

# Function to update the flashcard
def update_flashcard():
    if index[0] >= len(acronym_list):
        index[0] = 0
    current_acronym.set(acronym_list[index[0]][0])
    current_meaning.set("")
    index[0] += 1

# Function to show the meaning of the current acronym
def show_meaning():
    current_meaning.set(acronyms[current_acronym.get()])

# Create UI elements
acronym_label = tk.Label(app, textvariable=current_acronym, font=('Helvetica', 24))
acronym_label.pack(pady=20)

meaning_label = tk.Label(app, textvariable=current_meaning, font=('Helvetica', 18))
meaning_label.pack(pady=20)

show_button = tk.Button(app, text="Show Meaning", command=show_meaning)
show_button.pack(pady=20)

next_button = tk.Button(app, text="Next", command=update_flashcard)
next_button.pack(pady=20)

#Keyboard bindings 
app.bind('<Right>', lambda event: update_flashcard())
app.bind('<Enter>', lambda event: show_meaning())

#Initialize the first flashcard
update_flashcard()

#Start the application
app.mainloop()