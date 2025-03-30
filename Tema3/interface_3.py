import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__)) ))

from Interfata.tema_x import IterationBase
from tkinter import Toplevel, StringVar, OptionMenu, Label, Frame, Text, Scrollbar
from Tema3.implementation_ds import compute_system as compute_system_ds
from Tema3.implementation_crs import compute_system as compute_system_crs
from Tema3.sum.ds_matrix import compute_sum as compute_sum_ds
from Tema3.sum.crs_matrix import compute_sum as compute_sum_crs


class Iteration3(IterationBase):
    @staticmethod
    def solve_system():
        w = Toplevel()
        w.geometry("600x500")
        w.configure(bg="#6F7372")
        w.title("Solve System")

        # Create frame for controls
        control_frame = Frame(w, bg="#6F7372")
        control_frame.pack(pady=20)

        # Matrix selection
        Label(control_frame, text="Matrix:", bg="#6F7372", fg="white").pack(side='left', padx=10)
        matrix_var = StringVar(w)
        matrix_var.set("a_1")
        matrix_menu = OptionMenu(control_frame, matrix_var, "a_1", "a_2", "a_3", "a_4", "a_5", "a_t")
        matrix_menu.pack(side='left', padx=10)

        # Format selection
        Label(control_frame, text="Format:", bg="#6F7372", fg="white").pack(side='left', padx=10)
        format_var = StringVar(w)
        format_var.set("DS")
        format_menu = OptionMenu(control_frame, format_var, "DS", "CRS")
        format_menu.pack(side='left', padx=10)

        # Create text widget for results
        result_text = Text(w, height=20, width=60)
        result_text.pack(pady=20)
        
        # Add scrollbar
        scrollbar = Scrollbar(w, command=result_text.yview)
        scrollbar.pack(side='right', fill='y')
        result_text.configure(yscrollcommand=scrollbar.set)

        def solve():
            result_text.delete(1.0, 'end')  # Clear previous results
            matrix_num = matrix_var.get()
            matrix_path = f"Tema3/input_files/matrix/{matrix_num}.txt"
            vector_path = f"Tema3/input_files/vectors/b_{matrix_num[-1]}.txt"

            if format_var.get() == "DS":
                success, result = compute_system_ds(matrix_path, vector_path)
            else:
                success, result = compute_system_crs(matrix_path, vector_path)

            if success:
                result_text.insert('end', f"Matrix: {matrix_num}\n")
                result_text.insert('end', f"Format: {format_var.get()}\n\n")
                result_text.insert('end', f"Number of iterations: {result['iterations']}\n")
                result_text.insert('end', f"\nVerification: {result['verification']}\n\n")
                result_text.insert('end', "Solution xGS:\n")
                for i, val in enumerate(result['solution']):
                    result_text.insert('end', f"x[{i}] = {val:.6f}\n")
            else:
                result_text.insert('end', f"Error: {result}")

        solve_button = IterationBase.newButton(w, 0.5, 0.8, "Solve System", "White", "#426E93", solve)

    @staticmethod
    def compute_sum():
        w = Toplevel()
        w.geometry("600x500")
        w.configure(bg="#6F7372")
        w.title("Compute Sum")

        # Create frame for controls
        control_frame = Frame(w, bg="#6F7372")
        control_frame.pack(pady=20)

        # Format selection
        Label(control_frame, text="Format:", bg="#6F7372", fg="white").pack(side='left', padx=10)
        format_var = StringVar(w)
        format_var.set("DS")
        format_menu = OptionMenu(control_frame, format_var, "DS", "CRS")
        format_menu.pack(side='left', padx=10)

        # Create text widget for results
        result_text = Text(w, height=20, width=60)
        result_text.pack(pady=20)
        
        # Add scrollbar
        scrollbar = Scrollbar(w, command=result_text.yview)
        scrollbar.pack(side='right', fill='y')
        result_text.configure(yscrollcommand=scrollbar.set)

        def compute():
            result_text.delete(1.0, 'end')  # Clear previous results
            input_file_a = "Tema3/input_files/sum/a.txt"
            input_file_b = "Tema3/input_files/sum/b.txt"
            input_file_aplusb = "Tema3/input_files/sum/aplusb.txt"

            if format_var.get() == "DS":
                success, result = compute_sum_ds(input_file_a, input_file_b, input_file_aplusb)
            else:
                success, result = compute_sum_crs(input_file_a, input_file_b, input_file_aplusb)

            result_text.insert('end', f"Format: {format_var.get()}\n\n")
            if success:
                result_text.insert('end', f"\nVerification: {result['verification']}")
                result_text.insert('end', "Sum:\n")
                result_text.insert('end', result['result'])
            else:
                result_text.insert('end', f"Error: {result}")

        compute_button = IterationBase.newButton(w, 0.5, 0.8, "Compute Sum", "White", "#426E93", compute)

    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("400x300")
        w.configure(bg="#6F7372")
        w.title("Iteration 3")

        Iteration3.newButton(w, 0.5, 0.3, "Solve System", "White", "#426E93", Iteration3.solve_system)
        Iteration3.newButton(w, 0.5, 0.5, "Compute Sum", "White", "#426E93", Iteration3.compute_sum)
