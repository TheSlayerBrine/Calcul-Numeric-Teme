import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Interfata.tema_x import IterationBase
from tkinter import Toplevel, Label, Entry, Button, Text, Scrollbar, Frame, StringVar, OptionMenu, filedialog, IntVar, Scale, HORIZONTAL, messagebox
import numpy as np
import time
from Tema5.implementation_5 import (power_method, verify_symmetry, calculate_residual_norm)
from Tema5.sparse_matrix import (dump_to_file,generate_random_symmetric,read_matrix_from_file)


class Iteration5(IterationBase):
    @staticmethod
    def generate_random_matrix():
        w = Toplevel()
        w.geometry("800x600")
        w.configure(bg="#6F7572")
        w.title("Generate Random Sparse Symmetric Matrix")
        
        # Create frame for controls
        control_frame = Frame(w, bg="#6F7572")
        control_frame.pack(pady=20)
        
        # Matrix dimension
        Label(control_frame, text="Matrix Dimension (n):", bg="#6F7572", fg="white").grid(row=0, column=0, padx=10, pady=10)
        n_var = IntVar(w)
        n_var.set(500)  # Default dimension
        n_entry = Entry(control_frame, textvariable=n_var, width=8)
        n_entry.grid(row=0, column=1, padx=10, pady=10)
        
        # Density slider
        Label(control_frame, text="Density (%):", bg="#6F7572", fg="white").grid(row=0, column=2, padx=10, pady=10)
        density_var = IntVar(w)
        density_var.set(1)  # Default density 1%
        
        density_slider = Scale(
            control_frame,
            from_=1.0,        # Minim 0.1%
            to=5.0,           # Maxim 5%
            resolution=0.1,   # Pas de 0.1%
            orient=HORIZONTAL,
            label="Densitate (%)",
            variable=density_var
        )

        density_slider.grid(row=0, column=3, padx=10, pady=10)
        
        # Add a label to show the current density value
        density_label = Label(control_frame, textvariable=density_var, bg="#6F7572", fg="white")
        density_label.grid(row=0, column=4, padx=10, pady=10)
        
        # Create text widget for results
        result_text = Text(w, height=30, width=80)
        result_text.pack(pady=20)
        
        # Add scrollbar
        scrollbar = Scrollbar(w, command=result_text.yview)
        scrollbar.pack(side='right', fill='y')
        result_text.configure(yscrollcommand=scrollbar.set)
        
        def generate():
            try:
                n = n_var.get()
                if n < 2:
                    messagebox.showerror("Error", "Matrix dimension must be at least 2")
                    return
                    
                if n < 500:
                    response = messagebox.askquestion("Warning", 
                                                      "The assignment requires n > 500. Do you still want to continue with this smaller dimension?")
                    if response != 'yes':
                        return
                
                density = density_var.get() / 100.0  # Convert percentage to fraction
                
                result_text.delete(1.0, 'end')
                result_text.insert('end', f"Generating random sparse symmetric matrix with dimension {n} and density {density:.2%}...\n")
                
                start_time = time.time()
                values, col_indices, row_ptr, n = generate_random_symmetric(n, density)
                end_time = time.time()
                
                # Basic statistics
                num_nonzeros = len(values)
                density_actual = num_nonzeros / (n * n)
                is_sym = verify_symmetry(values, col_indices, row_ptr, n)
                
                result_text.insert('end', f"Matrix generation completed in {end_time - start_time:.2f} seconds\n\n")
                result_text.insert('end', f"Matrix dimension: {n}x{n}\n")
                result_text.insert('end', f"Non-zero elements: {num_nonzeros}\n")
                result_text.insert('end', f"Actual density: {density_actual:.4%}\n")
                result_text.insert('end', f"Is symmetric: {is_sym}\n\n")
                
                # Compute eigenvalue with power method
                result_text.insert('end', "Computing maximum eigenvalue using the power method...\n")
                start_time = time.time()
                lambda_max, v_max, iterations, residual_norm = power_method(values, col_indices, row_ptr, n)
                end_time = time.time()
                
                result_text.insert('end', f"Computation completed in {end_time - start_time:.2f} seconds\n\n")
                result_text.insert('end', f"Maximum eigenvalue: {lambda_max:.8f}\n")
                result_text.insert('end', f"Iterations: {iterations}\n")
                result_text.insert('end', f"Residual norm ||Av_max - λ_max·v_max||: {residual_norm:.8e}\n")
                
                # Option to save matrix
                save_frame = Frame(w, bg="#6F7572")
                save_frame.pack(pady=10)
                
                def save_matrix():
                    filename = filedialog.asksaveasfilename(
                        title="Save Matrix",
                        filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                        defaultextension=".txt"
                    )
                    if filename:
                        try:
                            dump_to_file(values, col_indices, row_ptr, n, filename)
                            messagebox.showinfo("Success", f"Matrix saved to {filename}")
                        except Exception as e:
                            messagebox.showerror("Error", f"Failed to save matrix: {str(e)}")
                
                Button(save_frame, text="Save Matrix", bg="#426E93", fg="white", 
                       command=save_matrix).pack(side='left', padx=10)
                
            except Exception as e:
                result_text.insert('end', f"Error: {str(e)}\n")
                import traceback
                result_text.insert('end', traceback.format_exc())
        
        # Add button to generate matrix
        Button(control_frame, text="Generate", bg="#426E93", fg="white", 
               command=generate).grid(row=0, column=5, padx=20, pady=10)
    
    @staticmethod
    def analyze_file_matrix():
        # Create a new window for file analysis
        file_window = Toplevel()
        file_window.title("Analyze Matrix from File")
        file_window.geometry("800x600")
        
        # Create a frame for the file selection
        file_frame = Frame(file_window)
        file_frame.pack(fill='x', padx=10, pady=10)
        
        # File selection
        file_path = StringVar()
        file_path.set("No file selected")
        Label(file_frame, text="Matrix File:", bg="#6F7572", fg="white").grid(row=0, column=0, padx=10, pady=10)
        file_label = Label(file_frame, textvariable=file_path, bg="#6F7572", fg="white", width=50)
        file_label.grid(row=0, column=1, padx=10, pady=10)
        
        # Create text widget for results
        result_text = Text(file_window, height=30, width=80)
        result_text.pack(pady=20)
        
        # Add scrollbar
        scrollbar = Scrollbar(file_window, command=result_text.yview)
        scrollbar.pack(side='right', fill='y')
        result_text.configure(yscrollcommand=scrollbar.set)
        
        def select_file():
            filename = filedialog.askopenfilename(
                title="Select Matrix File",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                initialdir="Tema5/input"
            )
            if filename:
                file_path.set(filename)
                
                # Clear previous results
                result_text.delete(1.0, 'end')
                result_text.insert('end', f"Reading matrix from {filename}...\n")
                
                try:
                    # Read matrix from file
                    start_time = time.time()
                    n, values, col_indices, row_ptr = read_matrix_from_file(filename)
                    end_time = time.time()
                    
                    # Display matrix properties
                    result_text.insert('end', f"\nMatrix Properties:\n")
                    result_text.insert('end', f"Dimension: {n}x{n}\n")
                    result_text.insert('end', f"Non-zero elements: {len(values)}\n")
                    result_text.insert('end', f"Density: {(len(values) / (n * n)):.2%}\n")
                    
                    # Verify symmetry
                    is_sym = verify_symmetry(values, col_indices, row_ptr, n)
                    result_text.insert('end', f"Symmetric: {is_sym}\n")
                    
                    if is_sym:
                        # Compute eigenvalues
                        result_text.insert('end', "\nComputing eigenvalues...\n")
                        lambda_max, v_max, iterations, residual_norm = power_method(values, col_indices, row_ptr, n)
                        
                        result_text.insert('end', f"\nResults:\n")
                        result_text.insert('end', f"Maximum eigenvalue: {lambda_max:.8f}\n")
                        result_text.insert('end', f"Iterations: {iterations}\n")
                        result_text.insert('end', f"Residual norm: {residual_norm:.8e}\n")
                    else:
                        result_text.insert('end', "\nMatrix is not symmetric. Cannot compute eigenvalues.\n")
                    
                except Exception as e:
                    result_text.insert('end', f"Error: {str(e)}\n")
                    import traceback
                    result_text.insert('end', traceback.format_exc())
        
        # Add button to select file
        Button(file_frame, text="Select File", bg="#426E93", fg="white", 
               command=select_file).grid(row=0, column=2, padx=20, pady=10)
    
    @staticmethod
    def compare_methods():
        """Compare power method results from generated and file-based matrices"""
        w = Toplevel()
        w.geometry("800x600")
        w.configure(bg="#6F7572")
        w.title("Compare File and Generated Matrices")
        
        # Create text widget for results
        result_text = Text(w, height=35, width=80)
        result_text.pack(pady=20)
        
        # Add scrollbar
        scrollbar = Scrollbar(w, command=result_text.yview)
        scrollbar.pack(side='right', fill='y')
        result_text.configure(yscrollcommand=scrollbar.set)
        
        result_text.insert('end', "Matrix Comparison\n")
        result_text.insert('end', "===============\n\n")
        result_text.insert('end', "This tool will compare eigenvalue computation between:\n")
        result_text.insert('end', "1. A randomly generated sparse symmetric matrix\n")
        result_text.insert('end', "2. A matrix loaded from one of the provided files\n\n")
        result_text.insert('end', "Click the button below to start the comparison.\n\n")
        
        def run_comparison():
            # Clear previous results
            result_text.delete(1.0, 'end')
            result_text.insert('end', "Running Matrix Comparison...\n\n")
            
            try:
                # 1. Generate a random sparse symmetric matrix
                n = 512  # Small enough for reasonable performance but large enough to satisfy requirements
                density = 0.01
                
                result_text.insert('end', f"Generating random matrix ({n}x{n}, density={density:.2%})...\n")
                values_gen, col_indices_gen, row_ptr_gen, n_gen = generate_random_symmetric(n, density)
                
                # Verify it's symmetric
                is_sym = verify_symmetry(values_gen, col_indices_gen, row_ptr_gen, n_gen)
                result_text.insert('end', f"Generated matrix is symmetric: {is_sym}\n")
                result_text.insert('end', f"Non-zero elements: {len(values_gen)}\n\n")
                
                # 2. Load a matrix from file
                filename = "Tema5/input/m_rar_sim_2025_512.txt"  # Use a medium-sized file
                result_text.insert('end', f"Reading matrix from file {filename}...\n")
                
                try:
                    n_file, values_file, col_indices_file, row_ptr_file = read_matrix_from_file(filename)
                    # Verify it's symmetric
                    is_sym = verify_symmetry(values_file, col_indices_file, row_ptr_file, n_file)
                    result_text.insert('end', f"File matrix is symmetric: {is_sym}\n")
                    result_text.insert('end', f"Non-zero elements: {len(values_file)}\n\n")
                    
                    # Compare eigenvalue computation
                    result_text.insert('end', "Computing eigenvalues...\n\n")
                    
                    # Generated matrix
                    start_time = time.time()
                    lambda_max_gen, v_max_gen, iterations_gen, residual_norm_gen = power_method(
                        values_gen, col_indices_gen, row_ptr_gen, n_gen
                    )
                    end_time = time.time()
                    result_text.insert('end', "Generated Matrix Results:\n")
                    result_text.insert('end', f"Maximum eigenvalue: {lambda_max_gen:.8f}\n")
                    result_text.insert('end', f"Iterations: {iterations_gen}\n")
                    result_text.insert('end', f"Residual norm: {residual_norm_gen:.8e}\n")
                    result_text.insert('end', f"Computation time: {end_time - start_time:.2f} seconds\n\n")
                    
                    # File matrix
                    start_time = time.time()
                    lambda_max_file, v_max_file, iterations_file, residual_norm_file = power_method(
                        values_file, col_indices_file, row_ptr_file, n_file
                    )
                    end_time = time.time()
                    result_text.insert('end', "File Matrix Results:\n")
                    result_text.insert('end', f"Maximum eigenvalue: {lambda_max_file:.8f}\n")
                    result_text.insert('end', f"Iterations: {iterations_file}\n")
                    result_text.insert('end', f"Residual norm: {residual_norm_file:.8e}\n")
                    result_text.insert('end', f"Computation time: {end_time - start_time:.2f} seconds\n")
                    
                except Exception as e:
                    result_text.insert('end', f"Error processing file matrix: {str(e)}\n")
                    import traceback
                    result_text.insert('end', traceback.format_exc())
                    
            except Exception as e:
                result_text.insert('end', f"Error: {str(e)}\n")
                import traceback
                result_text.insert('end', traceback.format_exc())
        
        # Add button to run comparison
        Button(w, text="Run Comparison", bg="#426E93", fg="white", 
               command=run_comparison).pack(pady=20)
    
    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("400x300")
        w.configure(bg="#6F7572")
        w.title("Iteration 5")
        
        Iteration5.newButton(w, 0.5, 0.3, "Generate Random Matrix", "White", "#426E93", Iteration5.generate_random_matrix)
        Iteration5.newButton(w, 0.5, 0.5, "Analyze File Matrix", "White", "#426E93", Iteration5.analyze_file_matrix)
        Iteration5.newButton(w, 0.5, 0.7, "Compare Methods", "White", "#426E93", Iteration5.compare_methods)
