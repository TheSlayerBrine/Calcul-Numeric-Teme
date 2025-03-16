from Interfata.tema_x import IterationBase
from tkinter import Toplevel
from Tema2.implementation_2 import *

Ainit = np.array([[4,3], [5,2.75]], dtype=float)
dU = [4,-1]
b = np.array([10,6], dtype=float)  
eps = 1e-9


def show_computed_LU(A, dU, eps):
    LU = compute_LU_decomposition(A, dU, eps)
    
    if isinstance(LU, str):  # Dacă e un mesaj de eroare, îl returnăm direct
        return f"Eroare: {LU}"
    
    n = LU.shape[0]
    L = np.eye(n)  # Inițializare L cu 1 pe diagonală
    U = np.zeros((n, n))  # Inițializare U cu 0
    
    for i in range(n):
        for j in range(n):
            if i > j:  
                L[i, j] = LU[i, j]  # Elemente sub diagonala principală
            else:  
                U[i, j] = LU[i, j]  # Elemente pe sau deasupra diagonalei

    
    return f"LU decomposition successful:\n{LU}\n Matrix L:\n {L}\n Matrix U:\n {U}"   

def show_determinant(A, dU, eps):
    LU = compute_LU_decomposition(A, dU, eps)
    
    if isinstance(LU, str):  # Dacă LU este un mesaj de eroare
        return f"Eroare: {LU}"
    
    detA = determinant_from_lu(LU)
    return f"Determinantul matricei A calculat cu LU este: {detA}, iar determinantul calculat cu funcția librăriei este: {np.linalg.det(A)}"

def show_sistem_solved_with_normes(Ainit, dU, b, eps):
    LU = compute_LU_decomposition(Ainit, dU, eps)
    
    if isinstance(LU, str):  # Dacă LU este un mesaj de eroare
        return f"Eroare: {LU}"
    
    xLU = solve_with_LU(Ainit, dU, b)
    norm_xLU = np.linalg.norm(np.dot(Ainit, xLU) - b, ord=2)  


    x_lib = np.linalg.solve(Ainit, b)
    norm_lib = np.linalg.norm(xLU - x_lib)


    x_inv = np.dot(np.linalg.inv(Ainit), b)
    norm_inv = np.linalg.norm(xLU - x_inv)

    return f"Solution from LU {xLU} with norm  {norm_xLU}\n Solution from library function: {x_lib} with norm ||xLU - xlib||2: {norm_lib}\n Solution from inv matrix : {x_inv} with  norm ||xLU - A^(-1) * b||2: {norm_inv}"



class Iteration2(IterationBase):
    @staticmethod
    def open():
        w = Toplevel()
        w.geometry("2024x576")
        w.configure(bg="#6F7272")
        w.title("Iteration 2")

        Iteration2.newButton(w, 0.5, 0.3, "Decompose in LU", "White", "#426E93", show_computed_LU(Ainit, dU, eps))
        Iteration2.newButton(w, 0.5, 0.4, "Calculate determinant", "White", "#426E93", show_determinant(Ainit, dU, eps))
        Iteration2.newButton(w, 0.5, 0.5, "Solve sistem and show normes", "White", "#426E93", show_sistem_solved_with_normes(Ainit, dU, b, eps))
