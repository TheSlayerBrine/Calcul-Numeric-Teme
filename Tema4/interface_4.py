import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Interfata.tema_x import IterationBase
from tkinter import Toplevel, StringVar, OptionMenu, Label, Frame, Text, Scrollbar, filedialog, Entry, Button, IntVar
from Tema4.implementation_4 import newton_schulz, li_li_variant1_inversion, li_li_variant2_inversion, non_square_newton_schulz
from Tema4.implementation_4 import generate_special_matrix, generate_inverse_from_formula, compare_formula_vs_iterative
from Tema4.implementation_4 import analyze_special_matrix_inverse, inverse_pattern_description
from Tema4.read_matrix import read_square_matrix,read_rectangular_matrix
import numpy as np


class Iteration4(IterationBase):
    # Class variable to store the deduced formula function
    formula_function = None
    
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
    def analyze_matrix_pattern():
        w = Toplevel()
        w.geometry("800x600")
        w.configure(bg="#6F7372")
        w.title("Special Matrix Pattern Analysis")

        # Create frame for controls
        control_frame = Frame(w, bg="#6F7372")
        control_frame.pack(pady=20)

        # Maximum dimension
        Label(control_frame, text="Maximum Dimension:", bg="#6F7372", fg="white").grid(row=0, column=0, padx=10, pady=10)
        max_n_var = IntVar(w)
        max_n_var.set(10)  # Default max dimension
        max_n_entry = Entry(control_frame, textvariable=max_n_var, width=5)
        max_n_entry.grid(row=0, column=1, padx=10, pady=10)

        # Create text widget for results
        result_text = Text(w, height=30, width=80)
        result_text.pack(pady=20)
        
        # Add scrollbar
        scrollbar = Scrollbar(w, command=result_text.yview)
        scrollbar.pack(side='right', fill='y')
        result_text.configure(yscrollcommand=scrollbar.set)

        def run_analysis():
            try:
                result_text.delete(1.0, 'end')
                
                max_n = max_n_var.get()
                
                if max_n < 2:
                    result_text.insert('end', "Error: Maximum dimension must be at least 2\n")
                    return
                
                result_text.insert('end', f"Analyzing special matrix pattern for dimensions 2 to {max_n}...\n\n")
                
                # Run the analysis
                results, formula = analyze_special_matrix_inverse(max_n=max_n, epsilon=1e-10, kmax=1000)
                
                # Store the formula function in the class variable for later use
                Iteration4.formula_function = formula
                
                # Describe the formula
                pattern_description = inverse_pattern_description(results)
                result_text.insert('end', pattern_description)
                
                result_text.insert(results)
                
            except Exception as e:
                result_text.insert('end', f"Error: {str(e)}\n")

        # Add button to run analysis
        Button(control_frame, text="Analyze Pattern", bg="#426E93", fg="white", 
               command=run_analysis).grid(row=0, column=2, padx=20, pady=10)
    
    @staticmethod
    def compare_formula_iterative():
        w = Toplevel()
        w.geometry("800x600")
        w.configure(bg="#6F7372")
        w.title("Formula vs Iterative Inversion Comparison")

        # Create frame for controls
        control_frame = Frame(w, bg="#6F7372")
        control_frame.pack(pady=20)

        # Matrix dimension
        Label(control_frame, text="Matrix Dimension:", bg="#6F7372", fg="white").grid(row=0, column=0, padx=10, pady=10)
        dimension_var = IntVar(w)
        dimension_var.set(5)  # Default dimension
        dimension_entry = Entry(control_frame, textvariable=dimension_var, width=5)
        dimension_entry.grid(row=0, column=1, padx=10, pady=10)

        # Method selection
        Label(control_frame, text="Method:", bg="#6F7372", fg="white").grid(row=0, column=2, padx=10, pady=10)
        method_var = StringVar(w)
        method_var.set("newton_schulz")
        methods = ["newton_schulz", "li_li_v1", "li_li_v2"]
        method_menu = OptionMenu(control_frame, method_var, *methods)
        method_menu.grid(row=0, column=3, padx=10, pady=10)

        # Create text widget for results
        result_text = Text(w, height=30, width=80)
        result_text.pack(pady=20)
        
        # Add scrollbar
        scrollbar = Scrollbar(w, command=result_text.yview)
        scrollbar.pack(side='right', fill='y')
        result_text.configure(yscrollcommand=scrollbar.set)

        def run_comparison():
            try:
                result_text.delete(1.0, 'end')
                
                n = dimension_var.get()
                method = method_var.get()
                
                if n < 2:
                    result_text.insert('end', "Error: Matrix dimension must be at least 2\n")
                    return
                
                # Check if formula has been deduced
                if Iteration4.formula_function is None:
                    result_text.insert('end', "Warning: Formula has not been deduced yet. Using default formula.\n\n")
                else:
                    result_text.insert('end', "Using previously deduced formula for comparison.\n\n")
                
                result_text.insert('end', f"Comparing formula-based and {method} algorithm inverses for {n}×{n} matrix\n\n")
                
                # Generate the special matrix
                A = generate_special_matrix(n)
                result_text.insert('end', "Original Matrix:\n")
                for row in A:
                    result_text.insert('end', " ".join(f"{val:.1f}" for val in row) + "\n")
                result_text.insert('end', "\n")
                
                # Perform comparison
                A, formula_inverse, iterative_inverse, difference_norm, iterations = compare_formula_vs_iterative(
                    n, method, epsilon=1e-10, kmax=1000, formula_function=Iteration4.formula_function)
                
                if iterative_inverse is None:
                    result_text.insert('end', f"The {method} algorithm failed to converge\n")
                    return
                
                # Display formula-based inverse
                result_text.insert('end', "Formula-Based Inverse:\n")
                for row in formula_inverse:
                    result_text.insert('end', " ".join(f"{val:.6e}" for val in row) + "\n")
                result_text.insert('end', "\n")
                
                # Display iterative inverse
                result_text.insert('end', f"Iterative Inverse ({method}, {iterations} iterations):\n")
                for row in iterative_inverse:
                    result_text.insert('end', " ".join(f"{val:.6e}" for val in row) + "\n")
                result_text.insert('end', "\n")
                
                # Display norm of difference
                I = np.eye(n)
                formula_error = np.linalg.norm(A @ formula_inverse - I, ord=1)
                iterative_error = np.linalg.norm(A @ iterative_inverse - I, ord=1)
                
                result_text.insert('end', f"Formula inverse error ||A×A⁻¹-I||₁: {formula_error:.2e}\n")
                result_text.insert('end', f"Iterative inverse error ||A×A⁻¹-I||₁: {iterative_error:.2e}\n")
                result_text.insert('end', f"Difference between inverses ||A⁻¹₁-A⁻¹₂||₁: {difference_norm:.2e}\n")
                
            except Exception as e:
                result_text.insert('end', f"Error: {str(e)}\n")

        # Add button to run comparison
        Button(control_frame, text="Compare", bg="#426E93", fg="white", 
               command=run_comparison).grid(row=0, column=4, padx=20, pady=10)

    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("400x400")
        w.configure(bg="#6F7372")
        w.title("Iteration 4")

        Iteration4.newButton(w, 0.5, 0.25, "Matrix Inversion", "White", "#426E93", Iteration4.compute_inverse)
        Iteration4.newButton(w, 0.5, 0.45, "Analyze Matrix Pattern", "White", "#426E93", Iteration4.analyze_matrix_pattern)
        Iteration4.newButton(w, 0.5, 0.65, "Compare Formula vs Iterative", "White", "#426E93", Iteration4.compare_formula_iterative)
