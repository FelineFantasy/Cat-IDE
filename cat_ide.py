import sys
import os
import platform
from tkinter import scrolledtext, filedialog, Menu, messagebox
import subprocess
import customtkinter as ctk
import shutil
import threading

def find_python():
    python = shutil.which("python")
    if python:
        return python

    possible_paths = [
        r"C:\Python313\python.exe",
        r"C:\Python312\python.exe",
        r"C:\Python311\python.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Python\Python313\python.exe"),
    ]
    for path in possible_paths:
        if os.path.exists(path):
            return path

    return sys.executable

AUTO_SAVE_INTERVAL = 5
auto_save_timer = None
needs_saving = False

def mark_dirty(event=None):
    global needs_saving
    needs_saving = True

def auto_save():
    global auto_save_timer, needs_saving
    
    if needs_saving:
        save()
        needs_saving = False
    
    auto_save_timer = threading.Timer(AUTO_SAVE_INTERVAL, auto_save)
    auto_save_timer.daemon = True
    auto_save_timer.start()

def save(event=None):
    if hasattr(save, 'current_file') and save.current_file:
        with open(save.current_file, "w", encoding="utf-8") as f:
            f.write(text.get("1.0", ctk.END))
    else:
        with open("temp_code.py", "w", encoding="utf-8") as f:
            f.write(text.get("1.0", ctk.END))

def open_file():
    file_path = filedialog.askopenfilename(
        title="Выбрать Python файл",
        filetypes=[("Python files", "*.py")]
    )
    if file_path:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        text.delete("1.0", ctk.END)
        text.insert("1.0", content)
        save.current_file = file_path
        root.title(f"Cat IDE - {file_path}")

def new_file():
    file_path = filedialog.asksaveasfilename(
        title="Создать новый .py файл",
        defaultextension=".py",
        filetypes=[("Python files", "*.py")]
    )
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("")
        text.delete("1.0", ctk.END)
        save.current_file = file_path
        root.title(f"Cat IDE - {file_path}")
        messagebox.showinfo("Успех", f"Создан файл: {file_path}")

def run():
    save()

    if hasattr(save, 'current_file') and save.current_file:
        file_to_run = save.current_file
    else:
        file_to_run = "temp_code.py"

    python = find_python()
    system = platform.system()

    if system == "Windows":
        subprocess.Popen(
            f'start cmd /c ""{python}" "{file_to_run}" & echo. & <nul set /p =Done! Press Enter to exit...& set /p ="',
            shell=True)
    elif system == "Darwin":
        subprocess.Popen(
            f'open -a Terminal "{python} {file_to_run}; echo -n \'Done! Press Enter to exit...\'; read"',
            shell=True)
    else:
        subprocess.Popen(
            f'x-terminal-emulator -e bash -c "{python} {file_to_run}; echo -n \'Done! Press Enter to exit...\'; read"',
            shell=True)

def show_menu(event):
    menu = Menu(root, tearoff=0)
    menu.add_command(label="Создать новый .py файл", command=new_file)
    menu.add_separator()
    menu.add_command(label="Открыть .py файл", command=open_file)
    menu.post(event.x_root, event.y_root)

def on_close():
    global auto_save_timer
    if auto_save_timer:
        auto_save_timer.cancel()
    if needs_saving:
        save()
    root.destroy()

root = ctk.CTk()
root.title("Cat IDE")
root.geometry("1200x800")

text = scrolledtext.ScrolledText(root, font=("Consolas", 12), bg="#1e1e1e", fg="white", insertbackground="white")
text.pack(fill=ctk.BOTH, expand=True)

button_run = ctk.CTkButton(
    root,
    text="▶",
    command=run,
    fg_color="green",
    hover_color="darkgreen",
    width=30,
    height=30
)
button_run.place(relx=1.0, x=-40, y=10, anchor="ne")

text.bind("<Button-3>", show_menu)

root.bind("<F5>", lambda event: run())
root.bind("<Control-s>", lambda event: save())
root.bind("<Control-n>", lambda event: new_file())

text.bind("<KeyRelease>", mark_dirty)

auto_save_timer = threading.Timer(AUTO_SAVE_INTERVAL, auto_save)
auto_save_timer.daemon = True
auto_save_timer.start()

root.protocol("WM_DELETE_WINDOW", on_close)

save.current_file = None

root.mainloop()
