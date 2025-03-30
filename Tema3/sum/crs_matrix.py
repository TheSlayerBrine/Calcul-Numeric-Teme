import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Tema3.read.compressed_row_storage import read_crs_matrix
from Tema3.display_matrix.crs_matrix import display_crs_matrix

def suma_matrici_crs(n, valori1, ind_col1, inceput_linii1, valori2, ind_col2, inceput_linii2):
    # Validări
    if len(inceput_linii1) != n + 1 or len(inceput_linii2) != n + 1:
        raise ValueError("Dimensiune incorectă pentru vectorul inceput_linii")
    
    if len(valori1) != inceput_linii1[-1] or len(valori2) != inceput_linii2[-1]:
        raise ValueError("Lungime incorectă pentru vectorul de valori")
    
    if len(ind_col1) != len(valori1) or len(ind_col2) != len(valori2):
        raise ValueError("Lungime incorectă pentru vectorul de indici de coloană")
    
    valori_sum = []
    ind_col_sum = []
    inceput_linii_sum = [0] * (n + 1)
    
    for i in range(n):
        row_values = {}
        
        # Verificăm ordinea coloanelor pentru prima matrice
        last_col = -1
        for idx in range(inceput_linii1[i], inceput_linii1[i + 1]):
            col = ind_col1[idx]
            if col <= last_col:
                raise ValueError(f"Coloanele nu sunt ordonate corect în prima matrice la linia {i}")
            last_col = col
            row_values[col] = row_values.get(col, 0) + valori1[idx]
        
        # Similar pentru a doua matrice
        last_col = -1
        for idx in range(inceput_linii2[i], inceput_linii2[i + 1]):
            col = ind_col2[idx]
            if col <= last_col:
                raise ValueError(f"Coloanele nu sunt ordonate corect în a doua matrice la linia {i}")
            last_col = col
            row_values[col] = row_values.get(col, 0) + valori2[idx]
        
        # Adăugăm valorile sortate
        for col in sorted(row_values.keys()):
            val = row_values[col]
            if abs(val) > 1e-10:  # Eliminăm valorile foarte apropiate de zero
                valori_sum.append(val)
                ind_col_sum.append(col)
        
        inceput_linii_sum[i + 1] = len(valori_sum)
    
    return valori_sum, ind_col_sum, inceput_linii_sum

def verifica_suma_matrici(n, valori_sum, ind_col_sum, inceput_linii_sum, 
                         valori_aplusb, ind_col_aplusb, inceput_linii_aplusb, epsilon=1e-6):
    try:
        # Validări pentru suma calculată
        if len(inceput_linii_sum) != n + 1 or len(inceput_linii_aplusb) != n + 1:
            raise ValueError("Dimensiune incorectă pentru vectorul inceput_linii")
        
        if len(valori_sum) != len(ind_col_sum) or len(valori_aplusb) != len(ind_col_aplusb):
            raise ValueError("Lungimi incorecte pentru vectorii de valori și indici")
        
        # Convertim ambele matrice în format dicționar pentru comparare
        matrix_sum = {}
        matrix_aplusb = {}
        
        # Convertim suma calculată
        for i in range(n):
            for idx in range(inceput_linii_sum[i], inceput_linii_sum[i + 1]):
                if ind_col_sum[idx] >= n:
                    raise ValueError(f"Index de coloană invalid în suma calculată: {ind_col_sum[idx]}")
                matrix_sum[(i, ind_col_sum[idx])] = valori_sum[idx]
        
        # Convertim matricea aplusb
        for i in range(n):
            for idx in range(inceput_linii_aplusb[i], inceput_linii_aplusb[i + 1]):
                if ind_col_aplusb[idx] >= n:
                    raise ValueError(f"Index de coloană invalid în matricea aplusb: {ind_col_aplusb[idx]}")
                matrix_aplusb[(i, ind_col_aplusb[idx])] = valori_aplusb[idx]
        
        # Verificăm toate pozițiile
        all_positions = set(matrix_sum.keys()) | set(matrix_aplusb.keys())
        for pos in all_positions:
            val_sum = matrix_sum.get(pos, 0)
            val_aplusb = matrix_aplusb.get(pos, 0)
            if abs(val_sum - val_aplusb) >= epsilon:
                print(f"Discrepanță la poziția {pos}: {val_sum} vs {val_aplusb}")
                return False
        
        return True
        
    except Exception as e:
        print(f"Eroare la verificarea sumei: {str(e)}")
        return False

def compute_sum(input_file_a, input_file_b, input_file_aplusb):
    try:
        # Read matrices
        n, valori_a, ind_col_a, inceput_linii_a = read_crs_matrix(input_file_a)
        n2, valori_b, ind_col_b, inceput_linii_b = read_crs_matrix(input_file_b)
        
        if n != n2:
            return False, "Matricele au dimensiuni diferite!"
        
        # Calculate sum
        valori_sum, ind_col_sum, inceput_linii_sum = suma_matrici_crs(
            n, valori_a, ind_col_a, inceput_linii_a,
            valori_b, ind_col_b, inceput_linii_b
        )
        
        # Get formatted display of sum only
        matrix_sum = display_crs_matrix(valori_sum, ind_col_sum, inceput_linii_sum)
        
        n_aplusb, valori_aplusb, ind_col_aplusb, inceput_linii_aplusb = read_crs_matrix(input_file_aplusb)
        
        if n != n_aplusb:
            return False, "Matricea rezultat are dimensiune diferită!"
        
        verification = verifica_suma_matrici(n, valori_sum, ind_col_sum, inceput_linii_sum,
                                     valori_aplusb, ind_col_aplusb, inceput_linii_aplusb)   
        
        return True, {
            'verification': verification,
            'result': matrix_sum
        }
        
    except Exception as e:
        return False, f"Eroare: {str(e)}"
