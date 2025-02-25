from Interfata.tema_x import IterationBase
from tkinter import Toplevel
from Tema6.implementation_6 import *


class Iteration6(IterationBase):
    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("6024x576")
        w.configure(bg="#6F7672")
        w.title("Iteration 6")

        Iteration6.newButton(w, 0.5, 0.3, "Iteration 6 - Action 1", "White", "#426E93", placeholder_function)
        Iteration6.newButton(w, 0.5, 0.4, "Iteration 6 - Action 2", "White", "#426E93", placeholder_function)
        Iteration6.newButton(w, 0.5, 0.5, "Iteration 6 - Action 3", "White", "#426E93", placeholder_function)
