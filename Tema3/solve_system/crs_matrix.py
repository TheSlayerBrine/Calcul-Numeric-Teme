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


def gauss_seidel_crs(n, valori, ind_col, inceput_linii, b, tolerance=1e-10, max_iterations=10000):
    xGS = [0] * n  # Inițializare cu 0 pentru toate elementele
    iterations = 0

    for k in range(max_iterations):
        max_diff = 0.0  

        for i in range(n):
            suma_ax = 0.0
            diag = 0.0  # Elementul diagonal
            
            start = inceput_linii[i]  
            end = inceput_linii[i + 1]  
            
            for idx in range(start, end):
                j = ind_col[idx]  
                if j == i:
                    diag = valori[idx]  # Identificăm valoarea de pe diagonală
                else:
                    suma_ax += valori[idx] * xGS[j]  # Calculăm suma A[i, j] * xGS[j]
            
            # Evităm împărțirea la zero
            if diag == 0:
                return "Failure: Zero diagonal element"
            
            # Calculăm noua valoare pentru xGS[i]
            new_x_i = (b[i] - suma_ax) / diag
            
            diff = abs(new_x_i - xGS[i])
            
            if diff > max_diff:
                max_diff = diff

            xGS[i] = new_x_i
        
        
        if (max_diff < tolerance) :
            break

        iterations += 1
    
    return xGS, iterations


def compute_residual_norm(self, x, b) -> float:
        Ax = [0.0] * self.n
        for i in range(self.n):
            for idx in range(self.start_line[i], self.start_line[i+1]):
                j = self.ind_col[idx]
                Ax[i] += self.values[idx] * x[j]

        residual = [Ax[i] - b[i] for i in range(self.n)]

        return max(abs(val) for val in residual)

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

    print(f"Norma ||GS - Ax - b||_inf = {eroare_maxima}")
    return eroare_maxima
