import time
import numpy as np
from Tema1.polynomials import polynomials


def compute_machine_precision():
    m = 1.0
    while 1.0 + 10**-m != 1.0:
        m += 1
    u = 10**-(m-1)
    if u + 1.0 !=1.0 and u/10 + 1.0 == 1.0:
        return u
    else:
        return 0

def verify_associativity(u):
    x, y, z = 1.0, u/10, u/10
    left_side, right_side = (x + y) + z, x + (y + z)
    print("(x+y)+z =", left_side)
    print("x+(y+z) =", right_side)
    if left_side == right_side:
        return True, left_side, right_side
    else:
        return False, left_side, right_side


def verify_multiplication_associativity(u):
    a, b, c = 0.1, u/10, u/10

    left_side = (a * b) * c
    right_side = a * (b * c)

    print("(a * b) * c =", left_side)
    print("a * (b * c) =", right_side)
    return left_side != right_side, left_side, right_side

diff, left, right = verify_multiplication_associativity(compute_machine_precision())



def compute_sin():
    top3_polynomials_per_x = []
    x_values = np.random.uniform(-np.pi/2, np.pi/2, 10000)
    for x in x_values:
        sin_true_value = np.sin(x)
        
        error_list = []
        for P in polynomials:
            error = abs(P(x) - sin_true_value)
            error_list.append((P.__name__, error))  

        error_list.sort(key=lambda item: item[1])
        
        top3_polynomials_per_x.append([polynomial for polynomial, _ in error_list[:3]])
    
    polynomial_frequency = {P.__name__: 0 for P in polynomials}
    for top_polynomials in top3_polynomials_per_x:
        for P in top_polynomials:
            polynomial_frequency[P] += 1

    sorted_polynomials = sorted(polynomial_frequency.items(), key=lambda item: item[1], reverse=True)

    timing = []
    for P in polynomials:
        start_time = time.time()
        for x in x_values:
            _=P(x)
        end_time = time.time()
        print(f"Time for {P.__name__}: {start_time} - {end_time} seconds")
        calculation_time = end_time - start_time
        timing.append((P.__name__, calculation_time))

    timing.sort(key=lambda item: item[1])
    print(timing)
        
    return sorted_polynomials,timing

