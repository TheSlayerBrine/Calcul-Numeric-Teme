import os
def read_b_vector(file):
    if os.path.exists(file):
        b = []
        with open(file, 'r') as f:
            n = int(f.readline().strip())  # Citim dimensiunea
            for line in f:
                line = line.strip()  # Eliminăm spațiile de la începutul și sfârșitul liniei
                if line:  # Verificăm dacă linia nu este goală
                    try:
                        b.append(float(line))  # Adăugăm valoarea în vector
                    except ValueError:
                        print(f"Eroare la conversia valorii: {line}")  # Mesaj de eroare pentru valori incorecte
                        continue  # Trecem la următoarea linie
    else:
            print(f"Fișierul {file} nu există.")
    return b