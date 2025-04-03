import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Interfata.tema_x import IterationBase
from tkinter import Toplevel, StringVar, OptionMenu, Label, Frame, Text, Scrollbar, filedialog
from Tema4.implementation_4 import newton_schulz, li_li_variant1_inversion, li_li_variant2_inversion, non_square_newton_schulz
from Tema4.read_matrix import read_square_matrix,read_rectangular_matrix
import numpy as np


class Iteration4(IterationBase):
    @staticmethod
    def compute_inverse():
        w = Toplevel()
        w.geometry("800x600")
        w.configure(bg="#6F7372")
        w.title("Matrix Inversion")

        # Create frame for controls
        control_frame = Frame(w, bg="#6F7372")
        control_frame.pack(pady=20)

        # Method selection
        Label(control_frame, text="Method:", bg="#6F7372", fg="white").pack(side='left', padx=10)
        method_var = StringVar(w)
        method_var.set("newton_schulz")
        methods = ["newton_schulz", "li_li_v1", "li_li_v2", "rectangular"]
        method_menu = OptionMenu(control_frame, method_var, *methods)
        method_menu.pack(side='left', padx=10)

        # Create text widget for results
        result_text = Text(w, height=30, width=80)
        result_text.pack(pady=20)
        
        # Add scrollbar
        scrollbar = Scrollbar(w, command=result_text.yview)
        scrollbar.pack(side='right', fill='y')
        result_text.configure(yscrollcommand=scrollbar.set)

        def select_file():
            filename = filedialog.askopenfilename(
                title="Select Matrix File",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                try:
                    result_text.delete(1.0, 'end')
                    result_text.insert('end', f"File: {filename}\n")
                    
                    method = method_var.get()

                    if method == "rectangular":
                        A = read_rectangular_matrix(filename)
                        X, iterations, rectangular_norm = non_square_newton_schulz(A)
                        result_text.insert('end', f"Final residual norm: {rectangular_norm:.2e}\n")
                    else:
                        A = read_square_matrix(filename)
                        I = np.eye(A.shape[0])
                        if method == "newton_schulz":
                            X, iterations = newton_schulz(A)
                            newton_schulz_norm = np.linalg.norm(X @ A - I, ord=1)
                            result_text.insert('end', f"Norm ||A*inv(A)-I||_1: {newton_schulz_norm:.2e}\n")
                        
                        elif method == "li_li_v1":
                            X, iterations = li_li_variant1_inversion(A)
                            li_li_v1_norm = np.linalg.norm(X @ A - I, ord=1)
                            result_text.insert('end', f"Norm ||A*inv(A)-I||_1: {li_li_v1_norm:.2e}\n")
                        
                        elif method == "li_li_v2":
                            X, iterations = li_li_variant2_inversion(A)
                            li_li_v2_norm = np.linalg.norm(X @ A - I, ord=1)
                            result_text.insert('end', f"Norm ||A*inv(A)-I||_1: {li_li_v2_norm:.2e}\n")
                   

                    result_text.insert('end', f"Iterations: {iterations}\n\n")
                                        
                    result_text.insert('end', "Inverse Matrix:\n")
                    for row in X:
                        result_text.insert('end', " ".join(f"{val:.6e}" for val in row) + "\n")
                    
                except Exception as e:
                    result_text.insert('end', f"Error: {str(e)}\n")

        select_button = IterationBase.newButton(w, 0.5, 0.8, "Select Matrix", "White", "#426E93", select_file)

    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("400x300")
        w.configure(bg="#6F7372")
        w.title("Iteration 4")

        Iteration4.newButton(w, 0.5, 0.4, "Matrix Inversion", "White", "#426E93", Iteration4.compute_inverse)
