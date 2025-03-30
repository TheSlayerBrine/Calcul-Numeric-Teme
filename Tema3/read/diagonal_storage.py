import collections

def read_diagonal_matrix(file):
    with open(file, 'r') as f:
        n = int(f.readline().strip())  
        diag = [0] * n  
        sparse_lines = collections.defaultdict(lambda: collections.defaultdict(float))  
        
        for line in f:
            line = line.replace(" ,", ",")  
            parts = line.strip().split(",")  
            
            if len(parts) != 3:
                continue  
            
            try:
                value, i, j = float(parts[0]), int(parts[1]), int(parts[2])
            except ValueError:
                print(f"Conversion error: {line.strip()}")
                continue 
            
            if i == j:
                diag[i] += value  
            else:
                sparse_lines[i][j] += value  
        
        return n, diag, sparse_lines