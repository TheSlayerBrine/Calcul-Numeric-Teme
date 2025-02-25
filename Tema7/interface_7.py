from Interfata.tema_x import IterationBase
from tkinter import Toplevel
from Tema7.implementation_7 import *


class Iteration7(IterationBase):
    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("7024x576")
        w.configure(bg="#6F7772")
        w.title("Iteration 7")

        Iteration7.newButton(w, 0.5, 0.3, "Iteration 7 - Action 1", "White", "#426E93", placeholder_function)
        Iteration7.newButton(w, 0.5, 0.4, "Iteration 7 - Action 2", "White", "#426E93", placeholder_function)
        Iteration7.newButton(w, 0.5, 0.5, "Iteration 7 - Action 3", "White", "#426E93", placeholder_function)
