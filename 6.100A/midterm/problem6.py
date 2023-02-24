def gcd(a, b):
    """
    a, b: two positive integers
    Returns the greatest common divisor of a and b
    """
    #YOUR CODE HERE

    if a % b == 0:
        return b
    else:
        return gcd(b, a % b)
