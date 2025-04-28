import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

# File to store tasks
TASKS_FILE = 'tasks.json'

# Load tasks from JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    return []

# Save tasks to JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)

# Add a new task
def add_task():
    if len(tasks) >= 20:
        messagebox.showwarning("Limit Reached", "You can only have a maximum of 20 tasks.")
        return

    task_description = simpledialog.askstring("Task Description", "Enter task description:")
    if not task_description:
        return

    task_date = simpledialog.askstring("Task Date", "Enter task date (YYYY-MM-DD):")
    if not task_date or not validate_date(task_date):
        messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
        return

    task_priority = simpledialog.askinteger("Task Priority", "Enter task priority (1-5):", minvalue=1, maxvalue=5)
    if task_priority is None:
        return

    task = {
        'description': task_description,
        'date': task_date,
        'priority': task_priority,
        'completed': False
    }
    tasks.append(task)
    save_tasks(tasks)
    update_task_list()

# Validate date format
def validate_date(date_text):
    try:
        datetime.strptime(date_text, '%Y-%m-%d')
        return True
    except ValueError:
        return False

# Mark task as complete
def mark_complete():
    selected_task_index = task_listbox.curselection()
    if not selected_task_index:
        messagebox.showwarning("Select Task", "Please select a task to mark as complete.")
        return

    task_index = selected_task_index[0]
    tasks[task_index]['completed'] = True
    save_tasks(tasks)
    update_task_list()

# Delete a task
def delete_task():
    selected_task_index = task_listbox.curselection()
    if not selected_task_index:
        messagebox.showwarning("Select Task", "Please select a task to delete.")
        return

    task_index = selected_task_index[0]
    del tasks[task_index]
    save_tasks(tasks)
    update_task_list()

# Update the task list display
def update_task_list():
    task_listbox.delete(0, tk.END)
    for task in tasks:
        status = "✔️" if task['completed'] else "❌"
        task_listbox.insert(tk.END, f"{status} {task['description']} (Due: {task['date']}, Priority: {task['priority']})")

# Initialize the main window
root = tk.Tk()
root.title("To-Do List App")

# Create a listbox to display tasks
task_listbox = tk.Listbox(root, width=50, height=15)
task_listbox.pack(pady=10)

# Create buttons for functionality
add_button = tk.Button(root, text="Add Task", command=add_task)
add_button.pack(pady=5)

complete_button = tk.Button(root, text="Mark Complete", command=mark_complete)
complete_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Task", command=delete_task)
delete_button.pack(pady=5)

# Load existing tasks
tasks = load_tasks()
update_task_list()

# Start the Tkinter event loop
root.mainloop()