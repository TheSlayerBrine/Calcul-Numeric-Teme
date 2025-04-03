import numpy as np

def read_square_matrix(filename):
    with open(filename, 'r') as f:
        first_line = f.readline().strip()
        if not first_line:
            raise ValueError("Empty file")
        n = int(first_line)  # Expecting a single integer for square matrix size
        
        data = []
        for line in f:
            if line.strip() == "":
                continue
            row = list(map(float, line.strip().split()))
            if len(row) != n:
                raise ValueError(f"Expected {n} elements in row, got {len(row)}")
            data.append(row)
        
        matrix = np.array(data)
        if matrix.shape != (n, n):
            raise ValueError(f"Expected matrix of shape {(n, n)}, got {matrix.shape}")
        return matrix

def read_rectangular_matrix(filename):
    with open(filename, 'r') as f:
        first_line = f.readline().strip()
        if not first_line:
            raise ValueError("Empty file")
        parts = first_line.split()
        if len(parts) != 2:
            raise ValueError("Invalid dimension header. Expected two integers for m and n.")
        
        m, n = int(parts[0]), int(parts[1])
        
        data = []
        for line in f:
            if line.strip() == "":
                continue
            row = list(map(float, line.strip().split()))
            if len(row) != n:
                raise ValueError(f"Expected {n} elements in row, got {len(row)}")
            data.append(row)
        
        matrix = np.array(data)
        if matrix.shape != (m, n):
            raise ValueError(f"Expected matrix of shape {(m, n)}, got {matrix.shape}")
        return matrix
