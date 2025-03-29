
import os
from read.read_b_vector import read_b_vector
from read.diagonal_storage import read_diagonal_matrix
from display_matrix.diagonal_storage_matrix import display_diagonal_matrix
from solve_system.ds import *


input_file_matrix = "C:\\Users\\Naomi\\Documents\\facultate\\INFO\\AN_3\\InfoSem2\\CN\\Calcul-Numeric-Teme\\Tema3\\input_files\\matrix\\a_1.txt"  # Fișierul cu matricea rară
input_file_b = "C:\\Users\\Naomi\\Documents\\facultate\\INFO\\AN_3\\InfoSem2\\CN\\Calcul-Numeric-Teme\\Tema3\\input_files\\vectors\\b_1.txt"  # Fișierul cu vectorul b

if os.path.exists(input_file_matrix):
    n, diag, sparse_lines = read_diagonal_matrix(input_file_matrix)
    #display_diagonal_matrix(n, diag, sparse_lines)
    
    if validate_diagonal_ds(diag):
        b = read_b_vector(input_file_b)
        xGS,iterations = gauss_seidel_sparse(n, diag, sparse_lines, b)
        
        print(f"Solutia aproximativă xGS: {xGS}")    
        print(f"converge in  {iterations} iteratii")
        print(f"verificare solutie: {verify_ds_solution(n,diag,sparse_lines,xGS,b)}")
    else:
        print("Matricea nu are toate elementele diagonale nenule!")
else:
    print(f"Fișierul {input_file_matrix} nu există.")

