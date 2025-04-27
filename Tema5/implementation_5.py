import numpy as np
from typing import Tuple
from Tema5.sparse_matrix import (get_value, matvec)


def power_method(
    values: list, col_indices: list, row_ptr: list, n: int,
    max_iterations: int = 10000,
    tolerance: float = 1e-10
) -> Tuple[float, np.ndarray, int, float]:
    """
    Implement the power method to find the dominant eigenvalue 
    and corresponding eigenvector of a matrix.
    
    Algorithm:
    1. Choose a random v vector in R^n with euclidean norm 1
    2. Compute w = Av
    3. Compute lambda = (w,v) (dot product)
    4. Update v = w/||w|| (normalize w)
    5. Repeat until convergence
    
    Parameters:
        values: List of non-zero values
        col_indices: List of column indices
        row_ptr: Row pointer array
        n: Matrix dimension
        max_iterations: Maximum number of iterations
        tolerance: Convergence tolerance
        
    Returns:
        (lambda_max, v_max, iterations, residual_norm):
        - lambda_max: Approximated maximum eigenvalue
        - v_max: Approximated eigenvector corresponding to lambda_max
        - iterations: Number of iterations performed
        - residual_norm: ||Av_max - lambda_max·v_max||
    """
    # 1. Choose a random v vector in R^n with euclidean norm 1
    v = np.random.rand(n)
    v = v / np.linalg.norm(v)
    
    lambda_old = 0
    
    for iteration in range(max_iterations):
        # 2. Compute w = Av
        w = matvec(values, col_indices, row_ptr, n, n, v)
        
        # 3. Compute lambda = (w,v) (dot product)
        lambda_max = v @ w
        
        # 4. Update v = w/||w|| (normalize w)
        w_norm = np.linalg.norm(w)
        if w_norm < 1e-15:  # Handle zero vector
            break
        v = w / w_norm
        
        # Check convergence on eigenvalue
        if abs(lambda_max - lambda_old) < tolerance:
            break
            
        lambda_old = lambda_max
    
    # Calculate residual norm ||Av_max - lambda_max·v_max||
    residual = matvec(values, col_indices, row_ptr, n, n, v) - lambda_max * v
    residual_norm = np.linalg.norm(residual)
    
    return lambda_max, v, iteration + 1, residual_norm


def verify_symmetry(values, col_indices, row_ptr, n):
    if n != len(row_ptr) - 1:
        return False
    
    for i in range(n):
        start_idx = row_ptr[i]
        end_idx = row_ptr[i + 1]
        for pos in range(start_idx, end_idx):
            j = col_indices[pos]
            if i != j:  # Only check off-diagonal elements
                if abs(values[pos] - get_value(values, col_indices, row_ptr, n, n, j, i)) > 1e-10:
                    return False
    return True


def calculate_residual_norm(values, col_indices, row_ptr, n, lambda_max, v_max):
    """
    Calculate the residual norm ||Av_max - lambda_max·v_max||.
    
    Parameters:
        values: List of non-zero values
        col_indices: List of column indices
        row_ptr: Row pointer array
        n: Matrix dimension
        lambda_max: Eigenvalue
        v_max: Eigenvector
        
    Returns:
        float: Residual norm
    """
    residual = matvec(values, col_indices, row_ptr, n, n, v_max) - lambda_max * v_max
    return np.linalg.norm(residual)

