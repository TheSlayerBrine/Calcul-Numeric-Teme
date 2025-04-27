import numpy as np
from typing import Optional

def create_sparse_matrix(n, m: Optional[int] = None):
    """
    Initialize a sparse matrix in CRS format.
    
    Parameters:
        n: Number of rows
        m: Number of columns (if None, assume square matrix)
        
    Returns:
        Tuple containing:
        - values: List of non-zero values
        - col_indices: List of column indices
        - row_ptr: Row pointer array
    """
    m = m if m is not None else n
    return [], [], [0] * (n + 1)

def set_value(values, col_indices, row_ptr, n, m, i, j, value):
    """
    Set value at position (i,j) in the sparse matrix.
    
    Parameters:
        values: List of non-zero values
        col_indices: List of column indices
        row_ptr: Row pointer array
        n: Number of rows
        m: Number of columns
        i: Row index
        j: Column index
        value: Value to set
    """
    if i < 0 or i >= n or j < 0 or j >= m:
        raise ValueError(f"Index out of bounds: ({i}, {j})")
    
    # Find the position to insert/update the value
    start_idx = row_ptr[i]
    end_idx = row_ptr[i + 1]
    
    # Search for existing entry in this row
    pos = start_idx
    while pos < end_idx and col_indices[pos] < j:
        pos += 1
        
    if pos < end_idx and col_indices[pos] == j:
        # Update existing value
        if abs(value) > 1e-15:
            values[pos] = value
        else:
            # Remove zero value
            values.pop(pos)
            col_indices.pop(pos)
            for k in range(i + 1, n + 1):
                row_ptr[k] -= 1
    elif abs(value) > 1e-15:
        # Insert new value
        values.insert(pos, value)
        col_indices.insert(pos, j)
        for k in range(i + 1, n + 1):
            row_ptr[k] += 1

def get_value(values, col_indices, row_ptr, n, m, i, j) :
    """
    Get value at position (i,j) in the sparse matrix.
    
    Parameters:
        values: List of non-zero values
        col_indices: List of column indices
        row_ptr: Row pointer array
        n: Number of rows
        m: Number of columns
        i: Row index
        j: Column index
        
    Returns:
        Value at position (i,j)
    """
    if i < 0 or i >= n or j < 0 or j >= m:
        raise ValueError(f"Index out of bounds: ({i}, {j})")
    
    start_idx = row_ptr[i]
    end_idx = row_ptr[i + 1]
    
    # Binary search in the row
    left, right = start_idx, end_idx - 1
    while left <= right:
        mid = (left + right) // 2
        if col_indices[mid] == j:
            return values[mid]
        elif col_indices[mid] < j:
            left = mid + 1
        else:
            right = mid - 1
            
    return 0.0


def matvec(values, col_indices, row_ptr, n, m, v):
    """
    Perform matrix-vector multiplication: A * v
    
    Parameters:
        values: List of non-zero values
        col_indices: List of column indices
        row_ptr: Row pointer array
        n: Number of rows
        m: Number of columns
        v: Input vector of length m
        
    Returns:
        Result vector of length n
    """
    if len(v) != m:
        raise ValueError(f"Vector length {len(v)} doesn't match matrix columns {m}")
    
    result = np.zeros(n)
    
    for i in range(n):
        start_idx = row_ptr[i]
        end_idx = row_ptr[i + 1]
        for pos in range(start_idx, end_idx):
            j = col_indices[pos]
            result[i] += values[pos] * v[j]
    
    return result


def read_matrix_from_file(fisier):
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
def generate_random_symmetric(n: int, density: float = 0.1) :
    if density <= 0 or density > 1:
        raise ValueError("Density must be between 0 and 1")

    values, col_indices, row_ptr = create_sparse_matrix(n)

    total_possible = n * n
    desired_nonzeros = int(density * total_possible)

    # Diagonal elements: always n
    for i in range(n):
        diag_value = 1000 + np.random.rand() * 1000
        set_value(values, col_indices, row_ptr, n, n, i, i, diag_value)

    nonzeros_added = n  # Diagonal elements already added

    # Number of off-diagonal non-zeros (counting pairs (i,j) and (j,i))
    nonzeros_offdiag_pairs = (desired_nonzeros - n) // 2

    added_pairs = set()  # To avoid adding the same (i,j) multiple times

    while len(added_pairs) < nonzeros_offdiag_pairs:
        i = np.random.randint(0, n)
        j = np.random.randint(0, n)
        if i == j:
            continue  # Skip diagonal

        # Ensure i < j to avoid duplicates
        if i > j:
            i, j = j, i

        if (i, j) not in added_pairs:
            added_pairs.add((i, j))
            value = np.random.rand() * 50

            set_value(values, col_indices, row_ptr, n, n, i, j, value)
            set_value(values, col_indices, row_ptr, n, n, j, i, value)

            nonzeros_added += 2

    return values, col_indices, row_ptr, n

def dump_to_file(values, col_indices, row_ptr, n, filename):
    """
    Write the sparse matrix to a file.
    
    Parameters:
        values: List of non-zero values
        col_indices: List of column indices
        row_ptr: Row pointer array
        n: Matrix dimension
        filename: Path to the output file
    """
    with open(filename, 'w') as f:
        f.write(f"{n}\n\n")
        
        # Write non-zero elements
        for i in range(n):
            start_idx = row_ptr[i]
            end_idx = row_ptr[i + 1]
            for pos in range(start_idx, end_idx):
                j = col_indices[pos]
                f.write(f"{values[pos]}, {i}, {j}\n") 