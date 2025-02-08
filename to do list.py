from flask import Flask, render_template, request, jsonify
import tkinter as tk
from tkinter import simpledialog, messagebox

app = Flask(__name__)

tasks = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_task():
    data = request.get_json()
    task = data.get('task')
    if task:
        tasks.append(task)
        return jsonify({'message': 'Task added!', 'tasks': tasks})
    return jsonify({'error': 'Task cannot be empty'}), 400

@app.route('/delete', methods=['POST'])
def delete_task():
    data = request.get_json()
    task = data.get('task')
    if task in tasks:
        tasks.remove(task)
        return jsonify({'message': 'Task removed!', 'tasks': tasks})
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})

def update_listbox():
    listbox.delete(0, tk.END)
    for task in tasks:
        listbox.insert(tk.END, task)

def add_task_gui():
    task = simpledialog.askstring("Add Task", "Enter a new task:")
    if task:
        tasks.append(task)
        update_listbox()

def remove_task_gui():
    selected_task = listbox.get(tk.ACTIVE)
    if selected_task in tasks:
        tasks.remove(selected_task)
        update_listbox()
    else:
        messagebox.showwarning("Error", "Task not found.")

def main_gui():
    global listbox
    root = tk.Tk()
    root.title("To-Do List")
    
    frame = tk.Frame(root)
    frame.pack(pady=20)
    
    listbox = tk.Listbox(frame, width=50, height=10)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.config(yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)
    
    button_frame = tk.Frame(root)
    button_frame.pack()
    
    add_button = tk.Button(button_frame, text="Add Task", command=add_task_gui)
    add_button.grid(row=0, column=0, padx=5)
    
    remove_button = tk.Button(button_frame, text="Remove Task", command=remove_task_gui)
    remove_button.grid(row=0, column=1, padx=5)
    
    exit_button = tk.Button(button_frame, text="Exit", command=root.quit)
    exit_button.grid(row=0, column=2, padx=5)
    
    root.mainloop()

if __name__ == '__main__':
    main_gui()
    