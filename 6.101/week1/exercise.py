
# How rewrite the following to be more pythonic?

def poly_evaluate(p, x):
    """
    Given an n-element list of numbers `p` that are polynomial
    coefficients, and a number `x`, returns the value of the
    polynomial p[0]x^0 + p[1]x^1 + ... + p[n-1]x^(n-1)
    """
    answer = 0
    for i in range(len(p)):
        answer += p[i] * x ** i
    return answer

