import tkinter as tk

def add_task():
    task = task_entry.get()
    if selected_task is not None:
        # Редактирование существующей задачи
        task_listBox.delete(selected_task)
        task_listBox.insert(selected_task, task)
        clear_selection()
    elif task:
        # Добавление новой задачи
        task_listBox.insert(tk.END, task)
    task_entry.delete(0, tk.END)

def delete_task():
    global selected_task
    selected_task = task_listBox.curselection()
    if selected_task:
        task_listBox.delete(selected_task[0])
        clear_selection()

def edit_task():
    global selected_task
    selected_task = task_listBox.curselection()
    if selected_task:
        task = task_listBox.get(selected_task[0])
        task_entry.delete(0, tk.END)
        task_entry.insert(0, task)

def clear_selection():
    global selected_task
    selected_task = None

root = tk.Tk()
root.title("Task list")
root.configure(background="deep sky blue")

selected_task = None  # Хранит текущий выбранный элемент для редактирования

text1 = tk.Label(root, text="Введите вашу задачу:", bg="deep sky blue")
text1.pack(pady=5)

task_entry = tk.Entry(root, width=30, bg="DeepPink4")
task_entry.pack(pady=10)

add_task_button = tk.Button(root, text="Добавить/Сохранить задачу", command=add_task)
add_task_button.pack(pady=5)

edit_button = tk.Button(root, text="Редактировать задачу", command=edit_task)
edit_button.pack(pady=5)

delete_button = tk.Button(root, text="Удалить задачу", command=delete_task)
delete_button.pack(pady=5)

task_listBox = tk.Listbox(root, height=10, width=50, bg="LightPink1")
task_listBox.pack(pady=10)

root.mainloop()

