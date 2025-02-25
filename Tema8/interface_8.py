from Interfata.tema_x import IterationBase
from tkinter import Toplevel
from Tema8.implementation_8 import *


class Iteration8(IterationBase):
    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("8024x576")
        w.configure(bg="#6F7872")
        w.title("Iteration 8")

        Iteration8.newButton(w, 0.5, 0.3, "Iteration 8 - Action 1", "White", "#426E93", placeholder_function)
        Iteration8.newButton(w, 0.5, 0.4, "Iteration 8 - Action 2", "White", "#426E93", placeholder_function)
        Iteration8.newButton(w, 0.5, 0.5, "Iteration 8 - Action 3", "White", "#426E93", placeholder_function)
