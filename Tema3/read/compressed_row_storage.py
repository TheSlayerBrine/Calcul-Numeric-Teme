import collections
import os

def read_crs_matrix(fisier):
    with open(fisier, 'r') as f:
        n = int(f.readline().strip())  
        temp_matrix = {}
        
        for linie in f:
            linie = linie.replace(" ,", ",")  
            parti = linie.strip().split(",")  
            
            if len(parti) != 3:
                continue  
            
            try:
                valoare, i, j = float(parti[0]), int(parti[1]), int(parti[2])
                if i < 0 or i >= n or j < 0 or j >= n:
                    print(f"Indici invalizi: i={i}, j={j}")
                    continue
                    
                if i not in temp_matrix:
                    temp_matrix[i] = {}
                temp_matrix[i][j] = temp_matrix[i].get(j, 0) + valoare
                
            except ValueError:
                print(f"Eroare la conversie: {linie.strip()}")
                continue  
        
        valori = []
        ind_col = []
        inceput_linii = [0] * (n + 1)
        
        for i in range(n):
            if i in temp_matrix:
                for j in sorted(temp_matrix[i].keys()):
                    valori.append(temp_matrix[i][j])
                    ind_col.append(j)
            inceput_linii[i + 1] = len(valori)
        
        return n, valori, ind_col, inceput_linii
