import tkinter as tk
from tkinter import messagebox

# Create main window
root = tk.Tk()
root.title("✅ To-Do List")
root.geometry("400x500")
root.config(bg="#f4f4f9")

# Task list
tasks = []

# Functions
def add_task():
    task = task_entry.get()
    if task != "":
        tasks.append(task)
        update_listbox()
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "You must enter a task!")

def delete_task():
    try:
        selected_index = listbox.curselection()[0]
        tasks.pop(selected_index)
        update_listbox()
    except IndexError:
        messagebox.showwarning("Warning", "Select a task to delete!")

def update_listbox():
    listbox.delete(0, tk.END)
    for task in tasks:
        listbox.insert(tk.END, task)

# Widgets
task_entry = tk.Entry(root, width=30, font=("Arial", 14))
task_entry.pack(pady=20)

add_button = tk.Button(root, text="Add Task", width=20, command=add_task)
add_button.pack(pady=5)

delete_button = tk.Button(root, text="Delete Selected Task", width=20, command=delete_task)
delete_button.pack(pady=5)

listbox = tk.Listbox(root, width=40, height=15, font=("Arial", 12))
listbox.pack(pady=20)

# Run app
root.mainloop()
