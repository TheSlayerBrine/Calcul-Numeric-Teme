import numpy as np
from Tema4.read_matrix import read_rectangular_matrix,read_square_matrix


def newton_schulz(A, epsilon = 1e-10, kmax = 1000):
    """
    Compute the inverse of a nonsingular square matrix A using the Newton-Schulz iteration:
         Vₖ₊₁ = Vₖ (2I - A Vₖ)
    Returns:
        (V, iterations): V approximates A⁻¹, iterations is the number of iterations.
    """
    n = A.shape[0]
    I = np.eye(n)
    A_inf = np.linalg.norm(A, ord=np.inf)
    A_1 = np.linalg.norm(A, ord=1)
    alpha = 1.0 / (A_1 * A_inf)
    V0 = V1 = alpha * A.T.copy()
    
    k = 1
    while(k < kmax):
        V0 = V1
        V1 = V0 @ (2 * I - A @ V0)
        difV = np.linalg.norm(V1 - V0, ord=1)
        if difV < epsilon:
            print("V1 aprox = A^-1 (soluția convergentă a fost găsită)")
            return V1, k
        if  difV > 10**10:
            print("Divergență detectată.")
            return None, k
        k += 1  

    print("Divergență: numărul maxim de iterații atins.")
    return None, k

def li_li_variant1_inversion(A, epsilon=1e-10, kmax=1000):
    """
    Compute the inverse of a nonsingular square matrix A using a Li–Li variant:
         Vₖ₊₁ = Vₖ (3Iₙ - AVₖ (3Iₙ - AVₖ))
    Returns:
         (V, iterations)
    """
    n = A.shape[0]
    I = np.eye(n)
    A_inf = np.linalg.norm(A, ord=np.inf)
    A_1 = np.linalg.norm(A, ord=1)
    alpha = 1.0 / (A_1 * A_inf)
    V0 = V1 = alpha * A.T.copy()
    
    k = 1
    while(k < kmax):
        V0 = V1
        
        inner_term = 3 * I - A @ V0
        full_term = 3 * I - A @ V0 @ inner_term
        V1 = V0 @ full_term

        difV = np.linalg.norm(V1 - V0, ord=1)
        if difV < epsilon:
            print("V1 aprox = A^-1 (soluția convergentă a fost găsită)")
            return V1, k
        if  difV > 10**10:
            print("Divergență detectată.")
            return None, k
        k += 1  

    print("Divergență: numărul maxim de iterații atins.")
    return None, k


def li_li_variant2_inversion(A, epsilon=1e-10, kmax=1000):
    """
    Compute the inverse of a nonsingular square matrix A using a second Li–Li variant:
         Vₖ₊₁ = ((Iₙ + 1/4(Iₙ - VₖA)(3Iₙ - VₖA)²)Vₖ
    Returns:
         (V, iterations)
    """
    n = A.shape[0]
    I = np.eye(n)
    A_inf = np.linalg.norm(A, ord=np.inf)
    A_1 = np.linalg.norm(A, ord=1)
    alpha = 1.0 / (A_1 * A_inf)
    V0 = V1 = alpha * A.T.copy()

    k = 1
    while(k < kmax):
        V0 = V1
        # Compute (Iₙ - VₖA)
        term1 = I - V0 @ A
        # Compute (3Iₙ - VₖA)
        term2 = 3 * I - V0 @ A
        # Compute (3Iₙ - VₖA)²
        term2_squared = term2 @ term2
        # Compute 1/4(Iₙ - VₖA)(3Iₙ - VₖA)²
        combined_term = 0.25 * term1 @ term2_squared
        # Compute (Iₙ + 1/4(Iₙ - VₖA)(3Iₙ - VₖA)²)
        final_term = I + combined_term
        # Compute final result
        V1 = final_term @ V0
        difV = np.linalg.norm(V1@A - I, ord=1)
        if difV < epsilon:
            print("V1 aprox = A^-1 (soluția convergentă a fost găsită)")
            return V1, k
        if  difV > 10**10:
            print("Divergență detectată.")
            return None, k
        k += 1  

    print("Divergență: numărul maxim de iterații atins.")
    return None, k



def non_square_newton_schulz(A, epsilon=1e-10, kmax=1000):
    """
    Pseudoinverse
    Approach: For full column rank matrices (m ≥ n), computes (A^T A)^(-1) A^T
              For full row rank matrices (m < n), computes A^T (A A^T)^(-1)
    
    Parameters:
        A: Input rectangular matrix (mxn)
        method: 'newton_schulz', 'li_li_v1', or 'li_li_v2'
    """
    m, n = A.shape
    
    if m >= n:  # More rows than columns - assume full column rank
        # Form square matrix A^T A (n×n)
        ATA = A.T @ A
        # Get inverse of ATA using one of the iterative methods
        V, iterations = newton_schulz(ATA, epsilon, kmax)
        # Form pseudoinverse as (A^T A)^(-1) A^T
        X = V @ A.T
        
    else:  # More columns than rows - assume full row rank
        # Form square matrix A A^T (m×m)
        AAT = A @ A.T
        
        # Get inverse of AAT using one of the iterative methods
        V, iterations = newton_schulz(AAT, epsilon, kmax)
            
        # Form pseudoinverse as A^T (A A^T)^(-1)
        X = A.T @ V
    
    # Validate the solution - the residual norms for rectangular matrices
    # If m≥n: ||X A - I_n||_1   (right inverse property)
    # If m<n: ||A X - I_m||_1   (left inverse property)
    if m >= n:
        I_n = np.eye(n)
        rectangular_norm = np.linalg.norm(X @ A - I_n, ord=1)
    else:
        I_m = np.eye(m)
        rectangular_norm = np.linalg.norm(A @ X - I_m, ord=1)
    
    return X, iterations, rectangular_norm  


