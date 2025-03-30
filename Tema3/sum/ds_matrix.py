import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Tema3.read.diagonal_storage import read_diagonal_matrix
from Tema3.display_matrix.diagonal_storage_matrix import display_diagonal_matrix
import collections

def verifica_suma_matrici(n, diag_sum, sparse_sum, diag_aplusb, sparse_aplusb, epsilon=1e-6):
    for i in range(n):
        if abs(diag_sum[i] - diag_aplusb[i]) >= epsilon:
            print(f"Discrepanță pe diagonală la poziția {i}: {diag_sum[i]} vs {diag_aplusb[i]}")
            return False
    
    all_rows = set(sparse_sum.keys()) | set(sparse_aplusb.keys())
    for i in all_rows:
        all_cols = set(sparse_sum[i].keys()) | set(sparse_aplusb[i].keys())
        for j in all_cols:
            val_sum = sparse_sum[i].get(j, 0)
            val_aplusb = sparse_aplusb[i].get(j, 0)
            if abs(val_sum - val_aplusb) >= epsilon:
                print(f"Discrepanță la poziția ({i},{j}): {val_sum} vs {val_aplusb}")
                return False
    return True

def suma_matrici_diagonal(n, diag1, sparse1, diag2, sparse2):
    diag_sum = [diag1[i] + diag2[i] for i in range(n)]
    sparse_sum = collections.defaultdict(lambda: collections.defaultdict(float))
    
    for i in sparse1:
        for j in sparse1[i]:
            sparse_sum[i][j] += sparse1[i][j]
    
    for i in sparse2:
        for j in sparse2[i]:
            sparse_sum[i][j] += sparse2[i][j]
    
    return diag_sum, sparse_sum

def compute_sum(input_file_a, input_file_b, input_file_aplusb):
    try:
        n, diag_a, sparse_a = read_diagonal_matrix(input_file_a)
        _, diag_b, sparse_b = read_diagonal_matrix(input_file_b)
        
        diag_sum, sparse_sum = suma_matrici_diagonal(n, diag_a, sparse_a, diag_b, sparse_b)
        
        # Get formatted display of sum only
        matrix_sum = display_diagonal_matrix(n, diag_sum, sparse_sum)
        
        n_aplusb, diag_aplusb, sparse_aplusb = read_diagonal_matrix(input_file_aplusb)
        verification = verifica_suma_matrici(n, diag_sum, sparse_sum, diag_aplusb, sparse_aplusb)
       
        return True, {
            'verification': verification,
            'result': matrix_sum
        }
        
    except Exception as e:
        return False, f"Eroare: {str(e)}"
