import collections

def read_diagonal_matrix(file):
    with open(file, 'r') as f:
        n = int(f.readline().strip())  # Read the size
        diag = [0] * n  # Initialize the diagonal vector
        sparse_lines = collections.defaultdict(lambda: collections.defaultdict(float))  # Sparse vectors with automatic summation
        
        for line in f:
            line = line.replace(" ,", ",")  # Remove spaces after commas
            parts = line.strip().split(",")  # Now correctly split by comma
            
            if len(parts) != 3:
                print(f"Incorrect line ignored: {line.strip()}")
                continue  
            
            try:
                value, i, j = float(parts[0]), int(parts[1]), int(parts[2])
            except ValueError:
                print(f"Conversion error: {line.strip()}")
                continue 
            
            if i == j:
                diag[i] += value  # Add to diagonal
            else:
                sparse_lines[i][j] += value  # Add to sparse matrix entries
        
        return n, diag, sparse_lines