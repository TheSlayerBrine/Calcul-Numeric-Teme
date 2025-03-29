
import os
from read.read_b_vector import read_b_vector
from read.compressed_row_storage import read_crs_matrix
from display_matrix.crs_matrix import display_crs_matrix
from solve_system.crs_matrix import *


input_file_matrix = "C:\\Users\\Naomi\\Documents\\facultate\\INFO\\AN_3\\InfoSem2\\CN\\Calcul-Numeric-Teme\\Tema3\\input_files\\matrix\\a_1.txt"  # Fișierul cu matricea rară
input_file_b = "C:\\Users\\Naomi\\Documents\\facultate\\INFO\\AN_3\\InfoSem2\\CN\\Calcul-Numeric-Teme\\Tema3\\input_files\\vectors\\b_1.txt"  # Fișierul cu vectorul b


if os.path.exists(input_file_matrix):
    n, valori, ind_col, inceput_linii = read_crs_matrix(input_file_matrix)
    #display_crs_matrix(valori, ind_col, inceput_linii)

    if validate_diagonal_crs(n, valori, ind_col, inceput_linii):
        b = read_b_vector(input_file_b)
        xGS, iterations = gauss_seidel_crs(n, valori, ind_col, inceput_linii, b)
        print(f"Solutia aproximativă xGS: {xGS}")
        print(f"converge in  {iterations} iteratii")
        print(f"verificare solutie: {verify_crs_solution(n,valori,ind_col,inceput_linii,xGS,b)}")
    else:
       print("Matricea nu are toate elementele diagonale nenule!")
else:
    print(f"Fișierul {input_file_matrix} nu există.")
