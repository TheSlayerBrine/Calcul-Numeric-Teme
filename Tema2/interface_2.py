from Interfata.tema_x import IterationBase
from tkinter import Toplevel
from Tema2.implementation_2 import *
from Tema2.bonus import *

A = np.array([
    [4,3], 
    [5,2.75]
    ], dtype=float)
dU = [4,-1]
b = np.array([10,6], dtype=float)  
eps = 1e-9


def show_computed_LU():
    LU = compute_LU_decomposition(A, dU, eps)
    
    if isinstance(LU, str):
        return f"Eroare: {LU}"
    
    n = LU.shape[0]
    L = np.eye(n)  #1 pe diag
    U = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            if i > j:  
                L[i, j] = LU[i, j]  #sub diag principala
            else:  
                U[i, j] = LU[i, j]  #pe sau deasupra diag principale

    
    return f"Descompunerea lai A in LU a avut succes:\n{LU}\nMatricea L:\n {L}\nMatricea U:\n {U}"   

def show_determinant():
    LU = compute_LU_decomposition(A, dU, eps)
    
    if isinstance(LU, str):
        return f"Eroare: {LU}"
    
    detA = determinant_from_lu(LU)
    return f"Determinantul matricei A calculat cu LU: {detA}\nDeterminantul calculat cu functia librariei: {np.linalg.det(A)}"

def show_sistem_solved_with_normes():
    LU = compute_LU_decomposition(A, dU, eps)
    
    if isinstance(LU, str):
        return f"Eroare: {LU}"
    
    xLU = solve_with_LU(LU, b)
    norm_xLU = np.linalg.norm(np.dot(A, xLU) - b, ord=2)  


    x_lib = np.linalg.solve(A, b)
    norm_lib = np.linalg.norm(xLU - x_lib)


    x_inv = np.dot(np.linalg.inv(A), b)
    norm_inv = np.linalg.norm(xLU - x_inv)

    return f"Solutia calculata cu descompunerea LU: {xLU}\ncu norma  {norm_xLU}\nSolutia calculata cu functia librariei: {x_lib}\ncu norma ||xLU - xlib||2: {norm_lib}\nSolutia calculata cu inversa matricei: {x_inv}\ncu norma ||xLU - A^(-1) * b||2: {norm_inv}"




def show_computed_LU_vectors():
    vector_L,vector_U = compute_LU_decomposition_vectors(A, dU, eps)

    if isinstance(vector_L, str) or isinstance(vector_U, str):
        return f"Eroare: {vector_L if isinstance(vector_L, str) else vector_U}"
    
    return f"Descompunerea lai A in vectorii L si U a avut succes.\nVectorul L:\n {vector_L}\nVectorul U:\n {vector_U}"   

def show_sistem_solved_vectors():
    vector_L,vector_U = compute_LU_decomposition_vectors(A, dU, eps)
    
    if isinstance(vector_L, str) or isinstance(vector_U, str):
        return f"Eroare: {vector_L if isinstance(vector_L, str) else vector_U}"
    
    xLU = solve_with_LU_vectors(A,vector_L,vector_U, b)
    return f"Solutia calculata cu descompunerea LU: {xLU}"


class Iteration2(IterationBase):
    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("2024x576")
        w.configure(bg="#6F7272")
        w.title("Iteration 2")

        Iteration2.newButton(w, 0.5, 0.3, "Descompunere in LU", "White", "#426E93", show_computed_LU)
        Iteration2.newButton(w, 0.5, 0.4, "Calculare determinant", "White", "#426E93", show_determinant)
        Iteration2.newButton(w, 0.5, 0.5, "Rezolvare sistem", "White", "#426E93", show_sistem_solved_with_normes)
        Iteration2.newButton(w, 0.5, 0.6, "Descompunere in vectori L, U", "White", "#426E93", show_computed_LU_vectors)
        Iteration2.newButton(w, 0.5, 0.7, "Rezolvare sistem cu vectori", "White", "#426E93", show_sistem_solved_vectors)
