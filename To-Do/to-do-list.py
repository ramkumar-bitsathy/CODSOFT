import tkinter as tk
from tkinter import ttk, messagebox
import csv

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")

        self.tasks = []

        # Frame
        self.frame = tk.Frame(root, padx=20, pady=20)
        self.frame.pack(expand=True, fill='both')

        # Task Entry
        self.task_label = tk.Label(self.frame, text="Task:", font=("Times New Roman", 14, "bold"))
        self.task_entry = tk.Entry(self.frame, width=30, font=("Times New Roman", 12))
        self.task_label.grid(row=0, column=0, pady=10, sticky="e")
        self.task_entry.grid(row=0, column=1, pady=10,columnspan=5)

        # Time Entry
        self.time_label = tk.Label(self.frame, text="Time:", font=("Times New Roman", 14, "bold"))
        self.time_entry = tk.Entry(self.frame, width=30, font=("Times New Roman", 12))
        self.time_label.grid(row=1, column=0, pady=10, sticky="e")
        self.time_entry.grid(row=1, column=1, pady=10,columnspan=5)

        # Task Treeview (Table)
        self.task_tree = ttk.Treeview(self.frame, columns=("Task", "Time", "Status"), show="headings")
        self.task_tree.heading("Task", text="Task", anchor="w")
        self.task_tree.column("Task", anchor="w", width=200)
        self.task_tree.heading("Time", text="Time", anchor="w")
        self.task_tree.column("Time", anchor="w", width=200)
        self.task_tree.heading("Status", text="Status", anchor="w")
        self.task_tree.column("Status", anchor="w", width=200)
        self.task_tree.grid(row=2, column=0, columnspan=5, pady=20)
        self.task_tree.tag_configure('completed_task', foreground='green', font=('Times New Roman', 12, 'bold'))
        self.task_tree.tag_configure('undone_task', foreground='red', font=('Times New Roman', 12, 'bold'))

        # Buttons
        self.add_button = tk.Button(self.frame, text="Add Task", command=self.add_task, font=("Times New Roman", 12))
        self.remove_button = tk.Button(self.frame, text="Remove Task", command=self.remove_task, font=("Times New Roman", 12))
        self.edit_button = tk.Button(self.frame, text="Edit Task", command=self.edit_task, font=("Times New Roman", 12))
        self.mark_completed_button = tk.Button(self.frame, text="Mark Comp", command=self.mark_completed, font=("Times New Roman", 12))
        self.add_button.grid(row=3, column=0)
        self.remove_button.grid(row=3, column=1)
        self.edit_button.grid(row=3, column=2)
        self.mark_completed_button.grid(row=3, column=4)

        # Load tasks from CSV file
        self.load_tasks()

    def add_task(self):
        task_text = self.task_entry.get().strip()
        time_text = self.time_entry.get().strip()

        if task_text and time_text:
            self.tasks.append({'Task': task_text, 'Time': time_text, 'Status': 'Incomplete'})
            self.task_tree.insert("", tk.END, values=(task_text, time_text, 'Incomplete'), tags=('undone_task',))
            self.task_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)

            # Save tasks to CSV file
            self.save_tasks()

    def remove_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            task_text = self.tasks.pop(int(self.task_tree.index(selected_item[0])))
            self.task_tree.delete(selected_item)
            messagebox.showinfo("Task Removed", f"Removed Task: {task_text['Task']} - {task_text['Time']}")

            # Save tasks to CSV file
            self.save_tasks()

    def edit_task(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            selected_task = self.tasks[int(self.task_tree.index(selected_item[0]))]
            edited_task_text = self.task_entry.get().strip()
            edited_time_text = self.time_entry.get().strip()

            if edited_task_text and edited_time_text:
                # Update the task in the list
                self.tasks[int(self.task_tree.index(selected_item[0]))] = {'Task': edited_task_text, 'Time': edited_time_text, 'Status': 'Incomplete'}

                # Update the task in the treeview
                self.task_tree.item(selected_item, values=(edited_task_text, edited_time_text, 'Incomplete'), tags=('undone_task',))

                messagebox.showinfo("Task Edited", "Task edited successfully.")

                # Save tasks to CSV file
                self.save_tasks()
            else:
                messagebox.showwarning("Input Error", "Both task and time must be provided.")

    def mark_completed(self):
        selected_item = self.task_tree.selection()
        if selected_item:
            task_index = int(self.task_tree.index(selected_item[0]))
            task = self.tasks[task_index]
            if task['Status'] == 'Incomplete':
                task['Status'] = 'Completed'
                self.task_tree.item(selected_item, values=(task['Task'], task['Time'], 'Completed'), tags=('completed_task',))
            else:
                messagebox.showinfo("Already Completed", "This task is already marked as completed.")

            # Save tasks to CSV file
            self.save_tasks()

    def load_tasks(self):
        try:
            with open('tasks.csv', 'r') as file:
                reader = csv.DictReader(file)
                self.tasks = [{'Task': row['Task'], 'Time': row['Time'], 'Status': row['Status']} for row in reader]
                for task in self.tasks:
                    if task['Status'] == 'Incomplete':
                        self.task_tree.insert("", tk.END, values=(task['Task'], task['Time'], 'Incomplete'), tags=('undone_task',))
                    else:
                        self.task_tree.insert("", tk.END, values=(task['Task'], task['Time'], 'Completed'), tags=('completed_task',))
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open('tasks.csv', 'w', newline='') as file:
            fieldnames = ['Task', 'Time', 'Status']
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            # Write header
            writer.writeheader()

            # Write tasks
            for task in self.tasks:
                writer.writerow(task)

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
