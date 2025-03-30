def display_crs_matrix(valori, ind_col, inceput_linii):
    n = len(inceput_linii) - 1
    matrix_str = f"Matrix in CRS format ({n}x{n}):\n\n"
    
    matrix_str += "Values array:      "
    matrix_str += " ".join(f"{val:6.2f}" for val in valori) + "\n"
    
    matrix_str += "Column indices:    "
    matrix_str += " ".join(f"{idx:6d}" for idx in ind_col) + "\n"
    
    matrix_str += "Row start indices: "
    matrix_str += " ".join(f"{idx:6d}" for idx in inceput_linii) + "\n"
    
    return matrix_str
