import os
import tkinter as tk
from tkinter import StringVar, IntVar, font, ttk
import random
import string
import csv

def generate_password():
    length = int(length_var.get())
    include_upper = include_upper_var.get()
    include_digits = include_digits_var.get()
    include_symbols = include_symbols_var.get()

    characters = string.ascii_lowercase
    if include_upper:
        characters += string.ascii_uppercase
    if include_digits:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation

    password = ''.join(random.choice(characters) for _ in range(length))
    password_var.set(password)

    label = password_label_var.get()

    # Add the generated password and label to the listbox
    #password_listbox.insert(tk.END, f"{label}: {password}")

    # Save the password and label to the CSV file in the current directory
    csv_path = os.path.join(os.getcwd(), 'passwords.csv')
    with open(csv_path, 'a', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow([label, password])

def view_generated_passwords():
    new_window = tk.Toplevel(app,bg="Pink")
    new_window.title("Generated Passwords")

    # Create Treeview widget for table display
    tree = ttk.Treeview(new_window, columns=('Label', 'Password'), show='headings', height=10)
    tree.heading('Label', text='Label')
    tree.heading('Password', text='Password')

    # Read passwords from the CSV file in the current directory
    csv_path = os.path.join(os.getcwd(), 'passwords.csv')
    with open(csv_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            tree.insert('', 'end', values=(row[0], row[1]))

    tree.pack()

# Create main window
app = tk.Tk()
app.title("Password Generator")
app.configure(bg="purple")

# Set screen size
screen_width = 600
screen_height = 400
app.geometry(f"{screen_width}x{screen_height}")

# Set font size
default_font = font.nametofont("TkDefaultFont")
default_font.configure(size=12)

# Create and pack widgets using grid layout
tk.Label(app, text="Label for Password:").grid(row=0, column=0, pady=10, padx=5, sticky='e')
password_label_var = StringVar()
password_label_entry = tk.Entry(app, textvariable=password_label_var)
password_label_entry.grid(row=0, column=1, pady=10, padx=5, sticky='w')

tk.Label(app, text="Password Length:").grid(row=0, column=2, pady=10, padx=5, sticky='e')
length_var = StringVar(value="12")  # Default length
length_entry = tk.Entry(app, textvariable=length_var)
length_entry.grid(row=0, column=3, pady=10, padx=5, sticky='w')

include_upper_var = IntVar(value=1)  # Include uppercase letters by default
include_upper_checkbox = tk.Checkbutton(app, text="Include Uppercase Letters", variable=include_upper_var,bg="pink")
include_upper_checkbox.grid(row=1, column=1, columnspan=4, pady=5, padx=5, sticky='w')

include_digits_var = IntVar(value=1)  # Include digits by default
include_digits_checkbox = tk.Checkbutton(app, text="Include Digits", variable=include_digits_var,bg="pink")
include_digits_checkbox.grid(row=2, column=1, columnspan=4, pady=5, padx=5, sticky='w')

include_symbols_var = IntVar(value=1)  # Include symbols by default
include_symbols_checkbox = tk.Checkbutton(app, text="Include Symbols", variable=include_symbols_var,bg="pink")
include_symbols_checkbox.grid(row=3, column=1, columnspan=4, pady=5, padx=5, sticky='w')

generate_button = tk.Button(app, text="Generate Password", command=generate_password,bg="yellow")
generate_button.grid(row=4, column=0, columnspan=4, pady=10)

password_var = StringVar()
password_entry = tk.Entry(app, textvariable=password_var, state='readonly', font=("Times New Roman", 14))  # Set font size
password_entry.grid(row=5, column=0, columnspan=4, pady=10)

view_button = tk.Button(app, text="View Generated Passwords", command=view_generated_passwords,bg="pink")
view_button.grid(row=6, column=0, columnspan=4, pady=10)

# Listbox to display generated passwords
"""
password_listbox = tk.Listbox(app, height=5, selectmode=tk.SINGLE, font=("Helvetica", 12))  # Set font size
password_listbox.grid(row=5, column=0, columnspan=4, pady=10)
"""
# Start the main loop
app.mainloop()
