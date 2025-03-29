
def validate_diagonal_ds(diag):
    for i, val in enumerate(diag):
        if val == 0:
            print(f"Error: Diagonal element d[{i}] is zero!")
            return False
    return True


def gauss_seidel_sparse(n, diag, sparse_lines, b, tolerance=1e-10, max_iterations=1000):
    xGS = [0] * n  
    iterations = 0

    for _ in range(max_iterations):
        max_diff = 0.0      
        for i in range(n):
            sum_ax = 0.0
            # Calculăm suma pentru A[i,j] * xGS[j] pentru j != i
            for j, value in sparse_lines[i].items():
                sum_ax += value * xGS[j]
            new_val = (b[i] - sum_ax) / diag[i]
            #print(f"iteratia {iterations}: x[{i}] {new_val}")
            diff = abs(new_val - xGS[i])
            
            if diff > max_diff:
                max_diff = diff
                
            xGS[i] = new_val
        
        iterations += 1
        
        if max_diff < tolerance:
            break

    return xGS, iterations


def verify_ds_solution(n, diag, sparse_lines, xGS, b):
    eroare_maxima = 0.0  # Inițializăm norma infinită

    for i in range(n):
        # Calculăm produsul Ax pentru linia i
        suma_ax = diag[i] * xGS[i]  # Elementul diagonal
        for j, value in sparse_lines[i].items():
            suma_ax += value * xGS[j]  # Elemente nenule din linia curentă
        
        eroare = abs(suma_ax - b[i])  # Diferența față de termenul b[i]
        eroare_maxima = max(eroare_maxima, eroare)  # Luăm maximul
    
    print(f"Norma ||GS - Ax - b||_inf = {eroare_maxima}")
    return eroare_maxima
