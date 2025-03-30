
def display_diagonal_matrix(n, diag, sparse_lines):
    matrix_str = f"Matrix in Diagonal Storage format ({n}x{n}):\n\n"
    for i in range(n):
        line = [(j, v) for j, v in sorted(sparse_lines[i].items())]
        matrix_str += f"d[{i}] = {diag[i]}\n"
        matrix_str += f" line {i}:  {line}\n"
    
    return matrix_str
