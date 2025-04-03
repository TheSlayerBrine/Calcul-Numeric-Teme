
def validate_diagonal_ds(diag):
    for i, val in enumerate(diag):
        if val == 0:
            print(f"Error: Diagonal element d[{i}] is zero!")
            return False
    return True

def gauss_seidel_ds(n, diag, sparse_lines, b, eps=1e-10, kmax=10000):
    xGS = [10] * n  
    k = 0  
    
    while k <= kmax:
        max_diff = 0.0  
        
        for i in range(n):
            sum_ax = 0.0
            
            for j, value in sparse_lines[i].items():
                sum_ax += value * xGS[j]
            
            new_val = (b[i] - sum_ax) / diag[i]
            diff = abs(new_val - xGS[i])
            
            if diff > max_diff:
                max_diff = diff
            
            xGS[i] = new_val
        
        print(f"Iterația {k}: xGS = {xGS}")
        print(verify_ds_solution(n, diag, sparse_lines, xGS, b))
        
        if max_diff < eps:
            print("Solutie atinsa")
            return xGS, k
        elif max_diff > 10**8:
            print("sistemul e divergent")
            return None, k
        
        k += 1
    
    print("Sistemul nu converge in numarul maxim de iteratii")
    return None, k

def verify_ds_solution(n, diag, sparse_lines, xGS, b):
    eroare_maxima = 0.0  

    for i in range(n):
        suma_ax = diag[i] * xGS[i]  
        for j, value in sparse_lines[i].items():
            suma_ax += value * xGS[j]  # Elemente nenule din linia curenta
        
        eroare = abs(suma_ax - b[i])  
        eroare_maxima = max(eroare_maxima, eroare)  
    
    print(f"Norma ||Ax - b||_inf = {eroare_maxima}")
    return eroare_maxima

def verify_first_column_ds(n, diag, sparse_lines):

    primul_element = diag[0]
    suma = 0.0
    
    for i in range(1, n):  
            for j, val in sparse_lines[i].items():
                if j == 0:
                    suma += val
    if(primul_element < suma):
        print("mai mic")
    else:
        print("mai mare")
    return primul_element, suma


