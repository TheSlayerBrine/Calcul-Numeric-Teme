import collections
import os

def read_crs_matrix(fisier):
    with open(fisier, 'r') as f:
        n = int(f.readline().strip())  # Citim dimensiunea
        valori = []  # Vectorul pentru valorile nenule
        ind_col = []  # Vectorul pentru indicii de coloană
        inceput_linii = [0] * (n + 1)  # Inițializăm început_linii
        nr_elemente = 0  # Contor pentru numărul total de elemente nenule

        for linie in f:
            linie = linie.replace(" ,", ",")  # Eliminăm spațiile după virgulă
            parti = linie.strip().split(",")  # Acum separăm corect după virgulă
            
            if len(parti) != 3:
                print(f"Linie incorectă ignorată: {linie.strip()}")
                continue  # Trecem la următoarea linie
            
            try:
                valoare, i, j = float(parti[0]), int(parti[1]), int(parti[2])
            except ValueError:
                print(f"Eroare la conversie: {linie.strip()}")
                continue  # Trecem la următoarea linie

            valori.append(valoare)  # Adăugăm valoarea nenulă
            ind_col.append(j)  # Adăugăm indicele de coloană
            inceput_linii[i + 1] += 1  # Incrementăm numărul de elemente pentru linia i
        
        # Calculăm început_linii(i+1) ca sumă cumulativă
        for i in range(1, n + 1):
            inceput_linii[i] += inceput_linii[i - 1]
        
        return n, valori, ind_col, inceput_linii
