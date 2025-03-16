import numpy as np

def validate_matrix(A):
    n = len(A)
    if not all(len(row) == n for row in A):
        raise ValueError("Matrice invalidă. Matricea introdusă trebuie să fie pătratică.")
    if np.linalg.det(A) == 0:
        raise ValueError("Matrice invalidă. Matricea introdusă trebuie să fie inversabilă.")

def validate_dU(dU, eps):
    if not all(abs(value) >= eps for value in dU):
        raise ValueError(f"Vector dU invalid. Toate valorile trebuie să fie mai mari decât 0 cu precizia {eps}.")

def L_idx(i, j):
    return i*(i+1)//2 + j

def U_idx(i, j):
    return j * (j + 1) // 2 + i

def lu_decomposition_vectors(A, dU):
    
    A = np.array(A, dtype=float)
    n = A.shape[0]

    size = n*(n+1)//2
    vector_L = np.zeros(size)  #  j<=i, diag = 1.   pe randuri   (0,0), (1,0), (1,1),(2,0), (2,1), (2,2) .......
    vector_U = np.zeros(size)  #  j>=i  pe coloane  (0,0), (0,1), (1,1), (0,2), (1,2), (2,2),(0,3),(1,3), (2,3), (3,3) ......
    
    
    for i in range(n):

        vector_U[U_idx(i,i)] = dU[i]
        
        for j in range(i):
            sum_LU = 0.0
            for k in range(j):
                L_ik = 1.0 if i == k else vector_L[L_idx(i, k)]
                U_kj = vector_U[U_idx(k, j)]
                sum_LU += L_ik * U_kj

            # L[i, j] = (A[i, j] - sum_LU) / U[j,j]
            U_jj = vector_U[U_idx(j, j)]
            value = (A[i, j] - sum_LU) / U_jj
            vector_L[L_idx(i, j)] = value
        
        vector_L[L_idx(i, i)] = 1.0
        
        for j in range(i+1, n):
            sum_LU = 0.0
            for k in range(i):
                L_ik = 1.0 if i == k else vector_L[L_idx(i, k)]
                U_kj = vector_U[U_idx(k, j)]
                sum_LU += L_ik * U_kj
            # U[i, j] = A[i,j] - sum_LU
            vector_U[U_idx(i, j)] = A[i, j] - sum_LU
        
        print(vector_L,vector_U)
    
    return vector_L, vector_U

def LU_product(vector_L, vector_U, n): 
    product = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            sum_value = 0
            for k in range(min(i, j) + 1):  # k trebuie să fie si in L si in U
                sum_value += vector_L[L_idx(i, k)] * vector_U[U_idx(k, j)]
            product[i, j] = sum_value
    return product



def forward_substitution_L(vector_L, b, n):
    y = np.zeros(n)
    for i in range(n):
        sum_Ly = 0.0
        for j in range(i):
            sum_Ly += vector_L[L_idx(i, j)] * y[j]
        y[i] = b[i] - sum_Ly
    return y

def backward_substitution_U(vector_U, y, n):
   
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        sum_Ux = 0.0
        for j in range(i+1, n):
            sum_Ux += vector_U[U_idx(i, j)] * x[j]
        U_ii = vector_U[U_idx(i, i)]
        x[i] = (y[i] - sum_Ux) / U_ii
    return x


def solve_with_LU_vectors(A,vector_L, vector_U, b):
    n = len(A)
    y = forward_substitution_L(vector_L, b, n)
    x = backward_substitution_U(vector_U, y, n)
    
    return x

def verify_lu_decomposition_vectors(A, vector_L, vector_U, eps):
    n = len(A)
    product = LU_product(vector_L, vector_U, n)
    if not np.allclose(A, product, atol=eps):
        raise ValueError("Descompunere LU incorecta. Produsul L*U diferă de A cu mai mult de {eps}.")
    

def compute_LU_decomposition_vectors(A, dU, eps):
    try:
        validate_matrix(A)
        validate_dU(dU, eps)
        
        vector_L, vector_U = lu_decomposition_vectors(A, dU)
        verify_lu_decomposition_vectors(A,vector_L,vector_U,eps)
        return vector_L,vector_U
    
    except ValueError as e:
        return str(e) 

