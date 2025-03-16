import numpy as np

def validate_matrix(A):
    n = len(A)
    
    if not all(len(row) == n for row in A):
        raise ValueError("Matrice invalida. Matricea introdusa trebuie sa fie patratica. ")

    if np.linalg.det(A) == 0:
        raise ValueError("Matrice invalida. Matricea introdusa trebuie sa fie inversabila. ")

def validate_dU(dU, eps):
    
    if not all(abs(value) >= eps for value in dU):
        raise ValueError(f"Vector dU invalid. Toate valorile trebuie sa fie mai mari decat 0 cu precizia {eps}.")

def lu_decomposition_inplace(A,dU):
    n = len(A)
    LU = A.astype(float).copy() 
    
    for i in range(n):
        LU[i, i] = dU[i]
        
        for j in range(i):  # Calcul elemente din L
            sum_LU = sum(LU[i, k] * LU[k, j] for k in range(j))
            LU[i, j] = (A[i, j] - sum_LU) / LU[j, j]
        
        for j in range(i + 1, n):  # Calcul elemente din U
            sum_LU = sum(LU[i, k] * LU[k, j] for k in range(i))
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
        raise ValueError("Descompunere LU incorecta. O valoare e diferita fata de cea originala cu mai mult de {eps}")


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


