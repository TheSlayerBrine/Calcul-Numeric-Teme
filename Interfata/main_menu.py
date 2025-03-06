import os
import sys
from tkinter import Tk, Button

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Tema1 import interface_1
from Tema2 import interface_2
from Tema3 import interface_3
from Tema4 import interface_4
from Tema5 import interface_5
from Tema6 import interface_6
from Tema7 import interface_7
from Tema8 import interface_8
from Tema5 import *


def main_menu():
    root = Tk()
    root.geometry("500x500")
    root.title("Main Menu")
    root.configure(bg="#6F7172")

    iterations = [
        ("Tema 1", interface_1.Iteration1.open),
        ("Tema 2", interface_2.Iteration2.open),
        ("Tema 3", interface_3.Iteration3.open),
        ("Tema 4", interface_4.Iteration4.open),
        ("Tema 5", interface_5.Iteration5.open),
        ("Tema 6", interface_6.Iteration6.open),
        ("Tema 7", interface_7.Iteration7.open),
        ("Tema 8", interface_8.Iteration8.open),
    ]

    for text, command in iterations:
        Button(root, text=text, command=command,
               font=("Roboto", 12), bg="#426E93", fg="white", width=30, height=2).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
