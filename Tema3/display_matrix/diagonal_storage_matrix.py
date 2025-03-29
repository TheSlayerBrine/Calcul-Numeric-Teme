
def display_diagonal_matrix(n, diag, sparse_lines):
    print("Matrix stored using method 1:")
    for i in range(n):
        line = [(j, v) for j, v in sorted(sparse_lines[i].items())]
        print(f"d[{i}] = {diag[i]}", f" line {i}:  ", line)
