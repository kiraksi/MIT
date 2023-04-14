def primes_list(N):
    '''
    N: an integer
    '''
    primes_list = []
    for i in range(2, N+1):
        isPrime = False
        for j in range(2, i):
            if i % j == 0:
                isPrime = True
        if not isPrime:
            primes_list.append(i)
    return primes_list
                
    
