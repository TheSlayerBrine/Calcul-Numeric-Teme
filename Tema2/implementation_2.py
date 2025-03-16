import numpy as np


def matrix_validation(A):
    n = len(A)
    
    if not all(len(x) == n for x in A):
        return "Invalid matrix. To make these operations the matrix has to be sqare"

    if np.linalg.det(A) == 0:
        return "Invalid matrix. To make these operations the matrix has to be non-singularity."
    
    return "OK"

def dU_validation(dU, eps):
    if not all([abs(dU[i]) >= eps for i in range(len(dU))]):
        return "Invalid dU vector. The values from this vector have to be grater then 0 with a precision of {eps}"
    return "OK"


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
    return np.allclose(A, A_reconstructed, atol=eps)


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

def solve_lu(A, dU, b):
    LU = lu_decomposition_inplace(A, dU)
    y = forward_substitution(LU, b)
    x = backward_substitution(LU, y)
    return x


def determinant_from_lu(LU):
    detU = np.prod(np.diag(LU))
    return detU  # det(A) = det(L)*det(U) = 1*det(U)


Ainit = np.array([[4,3], [5,2.75]], dtype=float)
dU = [4,-1]
b = np.array([10,6], dtype=float)  


LU = lu_decomposition_inplace(Ainit, dU)
print("LU Matrix:")
print(LU)

detA = determinant_from_lu(LU)
print(f"Determinantul matricei A: {detA}")
print(f"determinantul exact: {np.linalg.det(Ainit)}")

xLu = solve_lu(Ainit, dU, b)
print(f"Soluția aproximativă xLU: {xLu}")

error = np.linalg.norm(np.dot(Ainit, xLu) - b, ord=2)  


x_lib = np.linalg.solve(Ainit, b)
norm_LU_lib = np.linalg.norm(xLu - x_lib)

A_inv = np.linalg.inv(Ainit)
norm_LU_A_inv_b = np.linalg.norm(xLu - np.dot(A_inv, b))

print (f"Approximate solution: {xLu} with error: {error}")
print("Solution using inverse of matrix: ", x_lib)
print("Norm ||xLU - xlib||2: ", norm_LU_lib)
print("Norm ||xLU - A^(-1) * b||2: ", norm_LU_A_inv_b)



A_reconstructed = multiply_lu(LU)
print("Matricea A reconstruită:")
print(A_reconstructed)

is_valid = verify_lu_decomposition(Ainit, LU)
print("Verificare decompoziție LU corectă:", is_valid)
