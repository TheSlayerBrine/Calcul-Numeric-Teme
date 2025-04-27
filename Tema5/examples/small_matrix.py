import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import numpy as np
from Tema5.sparse_matrix import (create_sparse_matrix, set_value, generate_random_symmetric)
from Tema5.implementation_5 import (power_method,verify_symmetry)

def main():
    """Test the power method on a small matrix with known eigenvalues."""
    print("Testing power method on a small symmetric matrix")
    
    # Create a small matrix with known eigenvalues
    n = 5
    values, col_indices, row_ptr = create_sparse_matrix(n)
    
    # Set values for a diagonal matrix with known eigenvalues
    set_value(values, col_indices, row_ptr, n, n, 0, 0, 10.0)
    set_value(values, col_indices, row_ptr, n, n, 1, 1, 5.0)
    set_value(values, col_indices, row_ptr, n, n, 2, 2, 3.0)
    set_value(values, col_indices, row_ptr, n, n, 3, 3, 2.0)
    set_value(values, col_indices, row_ptr, n, n, 4, 4, 1.0)
    
    # Add some off-diagonal entries to make it more interesting but keep it symmetric
    set_value(values, col_indices, row_ptr, n, n, 0, 1, 1.5)
    set_value(values, col_indices, row_ptr, n, n, 1, 0, 1.5)
    set_value(values, col_indices, row_ptr, n, n, 0, 2, 0.5)
    set_value(values, col_indices, row_ptr, n, n, 2, 0, 0.5)
    set_value(values, col_indices, row_ptr, n, n, 1, 3, 0.7)
    set_value(values, col_indices, row_ptr, n, n, 3, 1, 0.7)
    set_value(values, col_indices, row_ptr, n, n, 2, 4, 0.3)
    set_value(values, col_indices, row_ptr, n, n, 4, 2, 0.3)
    
    # Verify it's symmetric
    is_sym = verify_symmetry(values, col_indices, row_ptr, n)
    print(f"Matrix is symmetric: {is_sym}")
    
    # Convert to numpy array for comparison
    dense_matrix = np.zeros((n, n))
    for i in range(n):
        start_idx = row_ptr[i]
        end_idx = row_ptr[i + 1]
        for pos in range(start_idx, end_idx):
            j = col_indices[pos]
            dense_matrix[i, j] = values[pos]
    
    # Compute eigenvalues with numpy for reference
    numpy_eigenvalues, numpy_eigenvectors = np.linalg.eig(dense_matrix)
    numpy_eigenvalues = np.sort(numpy_eigenvalues)[::-1]  # Sort in descending order
    
    print("\nReference eigenvalues from numpy.linalg.eig:")
    for i, eig in enumerate(numpy_eigenvalues):
        print(f"λ{i+1} = {eig:.8f}")
    
    # Use our power method implementation
    print("\nPower method approximation:")
    lambda_max, v_max, iterations, residual_norm = power_method(values, col_indices, row_ptr, n)
    
    print(f"Maximum eigenvalue: {lambda_max:.8f}")
    print(f"Numpy largest eigenvalue: {numpy_eigenvalues[0]:.8f}")
    print(f"Relative error: {abs(lambda_max - numpy_eigenvalues[0]) / abs(numpy_eigenvalues[0]):.8e}")
    print(f"Iterations: {iterations}")
    print(f"Residual norm ||Av_max - λ_max·v_max||: {residual_norm:.8e}")
    
    # Test on a randomly generated symmetric matrix
    print("\nTesting on a small random symmetric matrix:")
    values_rand, col_indices_rand, row_ptr_rand, n_rand = generate_random_symmetric(n=10, density=0.3)
    print(f"Matrix dimension: {n_rand}x{n_rand}")
    print(f"Non-zero elements: {len(values_rand)}")
    print(f"Is symmetric: {verify_symmetry(values_rand, col_indices_rand, row_ptr_rand, n_rand)}")
    
    lambda_max, v_max, iterations, residual_norm = power_method(values_rand, col_indices_rand, row_ptr_rand, n_rand)
    print(f"Maximum eigenvalue: {lambda_max:.8f}")
    print(f"Iterations: {iterations}")
    print(f"Residual norm ||Av_max - λ_max·v_max||: {residual_norm:.8e}")

if __name__ == "__main__":
    main() 