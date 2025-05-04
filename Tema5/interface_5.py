import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Interfata.tema_x import IterationBase
from tkinter import Toplevel, Label, Entry, Button, Text, Scrollbar, Frame, StringVar, OptionMenu, filedialog, IntVar, Scale, HORIZONTAL, messagebox
import numpy as np
import time
from Tema5.implementation_5 import (power_method, verify_symmetry, calculate_residual_norm, custom_rank, custom_condition_number)
from Tema5.sparse_matrix import (dump_to_file, generate_random_sparse_symmetric_positive1, read_matrix_from_file)


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
                values, col_indices, row_ptr, n = generate_random_sparse_symmetric_positive1(n, density)
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
    def svd_analysis():
        """Perform SVD analysis on a matrix"""
        w = Toplevel()
        w.geometry("800x600")
        w.configure(bg="#6F7572")
        w.title("SVD Analysis")
        
        # Create frame for controls
        control_frame = Frame(w, bg="#6F7572")
        control_frame.pack(pady=20)
        
        # Matrix dimensions
        Label(control_frame, text="Rows (n):", bg="#6F7572", fg="white").grid(row=0, column=0, padx=10, pady=10)
        n_var = IntVar(w)
        n_var.set(100)
        n_entry = Entry(control_frame, textvariable=n_var, width=8)
        n_entry.grid(row=0, column=1, padx=10, pady=10)
        
        Label(control_frame, text="Columns (p):", bg="#6F7572", fg="white").grid(row=0, column=2, padx=10, pady=10)
        p_var = IntVar(w)
        p_var.set(200)
        p_entry = Entry(control_frame, textvariable=p_var, width=8)
        p_entry.grid(row=0, column=3, padx=10, pady=10)
        
        # Create text widget for results
        result_text = Text(w, height=30, width=80)
        result_text.pack(pady=20)
        
        # Add scrollbar
        scrollbar = Scrollbar(w, command=result_text.yview)
        scrollbar.pack(side='right', fill='y')
        result_text.configure(yscrollcommand=scrollbar.set)
        
        def analyze():
            try:
                n = n_var.get()
                p = p_var.get()
                
                if n >= p:
                    messagebox.showerror("Error", "For SVD analysis, number of rows (n) must be less than columns (p)")
                    return
                
                result_text.delete(1.0, 'end')
                result_text.insert('end', f"Generating random matrix of size {n}x{p}...\n")
                
                # Create a random dense matrix
                A = np.random.rand(n, p)
                
                # Perform SVD
                start_time = time.time()
                U, S, Vt = np.linalg.svd(A, full_matrices=False)
                end_time = time.time()
                
                result_text.insert('end', f"SVD computation completed in {end_time - start_time:.2f} seconds\n\n")
                
                # Calculate rank using both methods
                rank_numpy = np.linalg.matrix_rank(A)
                rank_custom = custom_rank(S)
                
                # Calculate condition number using both methods
                cond_numpy = np.linalg.cond(A)
                cond_custom = custom_condition_number(S)
                
                # Display results
                result_text.insert('end', f"Matrix Properties:\n")
                result_text.insert('end', f"Size: {n}x{p}\n")
                result_text.insert('end', f"Rank (NumPy): {rank_numpy}\n")
                result_text.insert('end', f"Rank (Custom): {rank_custom}\n")
                result_text.insert('end', f"Condition Number (NumPy): {cond_numpy:.2e}\n")
                result_text.insert('end', f"Condition Number (Custom): {cond_custom:.2e}\n\n")
                
                # Display first 10 singular values
                result_text.insert('end', f"First 10 Singular Values:\n")
                for i, s in enumerate(S[:10]):
                    result_text.insert('end', f"σ{i+1}: {s:.8f}\n")
                
            except Exception as e:
                result_text.insert('end', f"Error: {str(e)}\n")
                import traceback
                result_text.insert('end', traceback.format_exc())
        
        # Add button to analyze
        Button(control_frame, text="Analyze", bg="#426E93", fg="white", 
               command=analyze).grid(row=0, column=4, padx=20, pady=10)
    
    @staticmethod
    def open():
        """Open the main interface window"""
        w = Toplevel()
        w.geometry("800x600")
        w.configure(bg="#6F7572")
        w.title("Numerical Methods - Assignment 5")
        
        # Create buttons for each functionality
        Button(w, text="Generate Random Matrix", bg="#426E93", fg="white", 
               command=Iteration5.generate_random_matrix).pack(pady=20)
        
        Button(w, text="Analyze Matrix from File", bg="#426E93", fg="white", 
               command=Iteration5.analyze_file_matrix).pack(pady=20)
        
        Button(w, text="SVD Analysis", bg="#426E93", fg="white", 
               command=Iteration5.svd_analysis).pack(pady=20)
