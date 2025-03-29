from Interfata.tema_x import IterationBase
from tkinter import Toplevel
from Tema3.implementation_ds import *
from Tema3.implementation_crs import *


class Iteration3(IterationBase):
    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("3024x576")
        w.configure(bg="#6F7372")
        w.title("Iteration 3")

        Iteration3.newButton(w, 0.5, 0.3, "Iteration 3 - Action 1", "White", "#426E93", placeholder_function)
        Iteration3.newButton(w, 0.5, 0.4, "Iteration 3 - Action 2", "White", "#426E93", placeholder_function)
        Iteration3.newButton(w, 0.5, 0.5, "Iteration 3 - Action 3", "White", "#426E93", placeholder_function)
