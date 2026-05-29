import sys
import platform
from tkinter import scrolledtext
import subprocess
import customtkinter as ctk


def save(event=None):
    with open("temp_code.py", "w", encoding="utf-8") as f:
        f.write(text.get("1.0", ctk.END))


def run():
    save()
    python = sys.executable

    system = platform.system()

    if system == "Windows":
        subprocess.Popen(
            f'start cmd /c "{python} temp_code.py & echo. & <nul set /p =Done! Press Enter to exit...& set /p ="',
            shell=True)
    elif system == "Darwin":
        subprocess.Popen(f'open -a Terminal "{python} temp_code.py; echo -n \'Done! Press Enter to exit...\'; read"',
                         shell=True)
    else:
        subprocess.Popen(
            f'x-terminal-emulator -e bash -c "{python} temp_code.py; echo -n \'Done! Press Enter to exit...\'; read"',
            shell=True)


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

root.bind("<F5>", lambda event: run())
root.bind("<Control-s>", lambda event: save())
text.bind("<KeyRelease>", lambda event: save())

root.mainloop()