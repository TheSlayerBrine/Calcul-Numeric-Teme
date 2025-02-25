from Interfata.tema_x import IterationBase
from tkinter import Toplevel
from Tema4.implementation_4 import *


class Iteration4(IterationBase):
    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("4024x576")
        w.configure(bg="#6F7472")
        w.title("Iteration 4")

        Iteration4.newButton(w, 0.5, 0.3, "Iteration 4 - Action 1", "White", "#426E93", placeholder_function)
        Iteration4.newButton(w, 0.5, 0.4, "Iteration 4 - Action 2", "White", "#426E93", placeholder_function)
        Iteration4.newButton(w, 0.5, 0.5, "Iteration 4 - Action 3", "White", "#426E93", placeholder_function)
