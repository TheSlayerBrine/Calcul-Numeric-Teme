from Interfata.tema_x import IterationBase
from tkinter import Toplevel
from Tema5.implementation_5 import *


class Iteration5(IterationBase):
    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("5024x576")
        w.configure(bg="#6F7572")
        w.title("Iteration 5")

        Iteration5.newButton(w, 0.5, 0.3, "Iteration 5 - Action 1", "White", "#426E93", placeholder_function)
        Iteration5.newButton(w, 0.5, 0.4, "Iteration 5 - Action 2", "White", "#426E93", placeholder_function)
        Iteration5.newButton(w, 0.5, 0.5, "Iteration 5 - Action 3", "White", "#426E93", placeholder_function)
