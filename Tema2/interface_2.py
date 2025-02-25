from Interfata.tema_x import IterationBase
from tkinter import Toplevel
from Tema2.implementation_2 import *



class Iteration2(IterationBase):
    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("2024x576")
        w.configure(bg="#6F7272")
        w.title("Iteration 2")

        Iteration2.newButton(w, 0.5, 0.3, "Iteration 2 - Action 1", "White", "#426E93", placeholder_function)
        Iteration2.newButton(w, 0.5, 0.4, "Iteration 2 - Action 2", "White", "#426E93", placeholder_function)
        Iteration2.newButton(w, 0.5, 0.5, "Iteration 2 - Action 3", "White", "#426E93", placeholder_function)
