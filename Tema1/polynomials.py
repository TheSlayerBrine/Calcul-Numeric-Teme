import math
import numpy as np
c1 = 1 / math.factorial(3)
c2 = 1 / math.factorial(5)
c3 = 1 / math.factorial(7)
c4 = 1 / math.factorial(9)
c5 = 1 / math.factorial(11)
c6 = 1 / math.factorial(13)
c_values = [c1, c2, c3, c4, c5, c6]


def compute_polynomial(x, coefficients):
    result = x
    power = x * x
    term = x
    sign = -1
    for c in coefficients:
        term *= power
        result += sign * c * term
        sign *= -1
    return result


#def P6(x): 
# y = x * x
# return x * (1 + y * (-0.16666 + y * (0.008333 + y * (-c3 + c4 * y))))


def P1(x): return compute_polynomial(x, c_values[:2])
def P2(x): return compute_polynomial(x, c_values[:3])
def P3(x): return compute_polynomial(x, c_values[:4])
def P4(x):return compute_polynomial(x, [0.166, 0.008333, c3,c4])
def P5(x):return compute_polynomial(x, [0.1666, 0.008333, c3,c4])
def P6(x):return compute_polynomial(x, [0.16666, 0.008333, c3,c4])
def P7(x): return compute_polynomial(x, c_values[:5])
def P8(x): return compute_polynomial(x, c_values[:6])

polynomials = [P1,P2,P3,P4,P5,P6,P7,P8]
