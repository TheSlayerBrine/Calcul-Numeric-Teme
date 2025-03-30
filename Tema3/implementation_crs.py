import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Tema3.read.read_b_vector import read_b_vector
from Tema3.read.compressed_row_storage import read_crs_matrix
from Tema3.display_matrix.crs_matrix import display_crs_matrix
from Tema3.solve_system.crs_matrix import *


def compute_system(matrix_file, vector_file):
    """
    Computes the solution of the system using CRS format
    """
    try:
        n, valori, ind_col, inceput_linii = read_crs_matrix(matrix_file)
        
        if validate_diagonal_crs(n, valori, ind_col, inceput_linii):
            b = read_b_vector(vector_file)
            xGS, iterations = gauss_seidel_crs(n, valori, ind_col, inceput_linii, b)
            if xGS is None:
                return False, "Sistemul este divergent"
            
            verification = verify_crs_solution(n, valori, ind_col, inceput_linii, xGS, b)
            return True, {
                'verification': verification,
                'iterations': iterations,
                'solution': xGS
            }
        else:
            return False, "Matricea nu are toate elementele diagonale nenule!"
            
    except Exception as e:
        return False, f"Eroare: {str(e)}"

