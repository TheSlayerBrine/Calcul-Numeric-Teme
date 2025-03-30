import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from Tema3.read.read_b_vector import read_b_vector
from Tema3.read.diagonal_storage import read_diagonal_matrix
from Tema3.display_matrix.diagonal_storage_matrix import display_diagonal_matrix
from Tema3.solve_system.ds import *


def compute_system(matrix_file, vector_file):
    
    try:
        n, diag, sparse_lines = read_diagonal_matrix(matrix_file)
        
        if validate_diagonal_ds(diag):
            b = read_b_vector(vector_file)
            xGS, iterations = gauss_seidel_ds(n, diag, sparse_lines, b)
            if xGS is None:
                return False, "Sistemul este divergent"
            
            verification = verify_ds_solution(n, diag, sparse_lines, xGS, b)
            return True, {
                'verification': verification,
                'iterations': iterations,
                'solution': xGS
            }
        else:
            return False, "Matricea nu are toate elementele diagonale nenule"
            
    except Exception as e:
        return False, f"Eroare: {str(e)}"
