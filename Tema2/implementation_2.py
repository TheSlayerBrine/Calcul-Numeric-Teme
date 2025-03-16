import numpy as np

def validate_matrix(A):
    """Verifică dacă matricea este pătratică și inversabilă."""
    n = len(A)
    
    if not all(len(row) == n for row in A):
        raise ValueError("Invalid matrix. The matrix must be square.")

    if np.linalg.det(A) == 0:
        raise ValueError("Invalid matrix. The matrix must be non-singular.")

def validate_dU(dU, eps):
    """Verifică dacă elementele din dU sunt mai mari decât eps."""
    if not all(abs(value) >= eps for value in dU):
        raise ValueError(f"Invalid dU vector. All values must be greater than {eps}.")

def lu_decomposition_inplace(A,dU):
    n = len(A)
    LU = A.astype(float).copy() 
    
    for i in range(n):
        LU[i, i] = dU[i]  # Setăm diagonala lui U conform lui dU
        
        for j in range(i):  # Calcul elemente din L
            sum_LU = sum(LU[i, k] * LU[k, j] for k in range(j))
            LU[i, j] = (A[i, j] - sum_LU) / LU[j, j]
        
        for j in range(i + 1, n):  # Calcul elemente din U
            sum_LU = sum(LU[i, k] * LU[k, j] for k in range(i))
            print(i,j,sum_LU)
            LU[i, j] = A[i, j] - sum_LU
    
    return LU

def multiply_lu(LU):
    n = LU.shape[0]
    A_reconstructed = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            sum_LU = 0
            for k in range(n):
                L_ik = LU[i, k] if k < i else (1.0 if k == i else 0)  # Elemente din L
                U_kj = LU[k, j] if k <= j else 0  # Elemente din U
                sum_LU += L_ik * U_kj
            A_reconstructed[i, j] = sum_LU
    
    return A_reconstructed

def verify_lu_decomposition(A,LU,eps=1e-10):
    A_reconstructed = multiply_lu(LU)
    if not np.allclose(A, A_reconstructed, atol=eps):
        raise ValueError("LU decomposition was incorect. A value is diffrent then the original matrix with more then {eps}")


def compute_LU_decomposition(A, dU, eps):
    try:
        validate_matrix(A)
        validate_dU(dU, eps)
        
        LU = lu_decomposition_inplace(A, dU)
        verify_lu_decomposition(A,LU)
        return LU
    
    except ValueError as e:
        return str(e) 
    

def forward_substitution(LU, b):
    n = len(LU)
    y = np.zeros(n)
    for i in range(n):
        y[i] = b[i] - sum(LU[i, j] * y[j] for j in range(i))
    return y

def backward_substitution(LU, y):
    n = len(LU)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(LU[i, j] * x[j] for j in range(i + 1, n))) / LU[i, i]
    return x

def solve_with_LU(A, dU, b):
    LU = lu_decomposition_inplace(A, dU)
    y = forward_substitution(LU, b)
    x = backward_substitution(LU, y)
    return x

def determinant_from_lu(LU):
    detU = np.prod(np.diag(LU))
    return detU  # det(A) = det(L)*det(U) = 1*det(U)


def show_determinant(A, dU, eps):
    LU = compute_LU_decomposition(A, dU, eps)
    
    if isinstance(LU, str):  # Dacă LU este un mesaj de eroare
        return f"Eroare: {LU}"
    
    detA = determinant_from_lu(LU)
    return f"Determinantul matricei A calculat cu LU este: {detA}, iar determinantul calculat cu funcția librăriei este: {np.linalg.det(A)}"

def show_computed_LU(A, dU, eps):
    LU = compute_LU_decomposition(A, dU, eps)
    
    if isinstance(LU, str):  # Dacă e un mesaj de eroare, îl returnăm direct
        return f"Eroare: {LU}"
    return f"LU decomposition successful:\n{LU}"
    

def show_sistem_solved_with_normes(Ainit, dU, b, eps):
    LU = compute_LU_decomposition(Ainit, dU, eps)
    
    if isinstance(LU, str):  # Dacă LU este un mesaj de eroare
        return f"Eroare: {LU}"
    
    xLU = solve_with_LU(Ainit, dU, b)
    norm_xLU = np.linalg.norm(np.dot(Ainit, xLU) - b, ord=2)  


    x_lib = np.linalg.solve(Ainit, b)
    norm_lib = np.linalg.norm(xLU - x_lib)


    x_inv = np.dot(np.linalg.inv(Ainit), b)
    norm_inv = np.linalg.norm(xLU - x_inv)

    return f"Solution from LU {xLU} with norm  {norm_xLU}\n Solution from library function: {x_lib} with norm ||xLU - xlib||2: {norm_lib}\n Solution from inv matrix : {x_inv} with  norm ||xLU - A^(-1) * b||2: {norm_inv}"


def placeholder_function():
    print("Functionality will be implemented here.")
    return"Functionality will be implemented here."