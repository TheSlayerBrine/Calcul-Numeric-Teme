def validate_diagonal_crs(n, valori, ind_col, inceput_linii):
    for i in range(n):
        start = inceput_linii[i]  
        end = inceput_linii[i + 1]  
        diag = 0.0
        
        for idx in range(start, end):
            if ind_col[idx] == i:
                diag = valori[idx]
                break
        
        if diag == 0:
            print(f"Error: Diagonal element d[{i}] is zero!") 
            return False
    return True


def gauss_seidel_crs(n, valori, ind_col, inceput_linii, b, eps=1e-10, kmax=10000):
    xGS = [0] * n  # Inițializare soluție
    k = 0  # Număr de iterații
    
    while k <= kmax:
        max_diff = 0.0  

        for i in range(n):
            suma_ax = 0.0
            diag = 0.0  
            
            start = inceput_linii[i]  
            end = inceput_linii[i + 1]  
            
            for idx in range(start, end):
                j = ind_col[idx]  
                if j == i:
                    diag = valori[idx]  
                else:
                    suma_ax += valori[idx] * xGS[j]  # suma A[i, j] * xGS[j]
            
            new_x_i = (b[i] - suma_ax) / diag
            
            diff = abs(new_x_i - xGS[i])
            if diff > max_diff:
                max_diff = diff

            xGS[i] = new_x_i

        
        print(f"Iterația {k}: xGS = {xGS}")
        print(verify_crs_solution(n, valori, ind_col, inceput_linii, xGS, b))
        if max_diff < eps:
            print("xc aprox = x* (soluția convergentă a fost găsită)")
            return xGS, k
        elif max_diff > 10**8:
            print("Divergență detectată.")
            return None, k

        k += 1
    
    print("Divergență: numărul maxim de iterații atins.")
    return None, k


def verify_crs_solution(n, valori, ind_col, inceput_linii, xGS, b):
    eroare_maxima = 0.0

    for i in range(n):
        suma_ax = 0.0
        start = inceput_linii[i]
        end = inceput_linii[i + 1]
        
        for idx in range(start, end):
            j = ind_col[idx]
            suma_ax += valori[idx] * xGS[j]

        eroare = abs(suma_ax - b[i])
        eroare_maxima = max(eroare_maxima, eroare)

    print(f"Norma  = {eroare_maxima}")
    return eroare_maxima


def verify_first_column(n, valori, ind_col, inceput_linii):

    suma = 0.0
    for i in range(1, n):  
        for k in range(inceput_linii[i], inceput_linii[i + 1]):
            if ind_col[k] == 0:
                suma += valori[k]
                
    primul_element = valori[0] 
    if(primul_element < suma):
        print("mai mic")
    else:
        print("mai mare")
    return primul_element, suma



