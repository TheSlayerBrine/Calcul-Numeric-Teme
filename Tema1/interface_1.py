from Interfata.tema_x import IterationBase
from tkinter import Toplevel
from Tema1.implementation_1 import *

class Iteration1(IterationBase):
    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("1024x576")
        w.configure(bg="#6F7172")
        w.title("Iteration 1")

        Iteration1.newButton(w, 0.5, 0.3, "Iteration 1 - Action 1", "White", "#426E93", placeholder_function)
        Iteration1.newButton(w, 0.5, 0.4, "Iteration 1 - Action 2", "White", "#426E93", placeholder_function)
        Iteration1.newButton(w, 0.5, 0.5, "Iteration 1 - Action 3", "White", "#426E93", placeholder_function)
