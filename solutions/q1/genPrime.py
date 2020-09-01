import sys
import random
import math


def exp(x, e, m=None):
    '''
    Calculates x ** e % m. If m is ommitted then the function is equivalent to just x ** e.
        x:  Base.
        e:  Exponent.
        m:  Modulo.
        Time:   O(log n) (assuming O(1) integer multiplication)
        Space:  O(1)
            where:
            n = e
    '''
    res = 1
    while e:
        if e & 1:
            res *= x
            if m:
                res %= m
        e >>= 1
        x *= x
        if m:
            res %= m
    if m:
        res %= m
    return res


def is_prime(n, k=64):
    '''
    Performs Miller-Rabin primality test on n for k iterations.
        n:  Number to test.
        k:  Number of iterations to perform.
        Time:   O(log n + klog^3 n)
        Space:  O(1)
    '''
    if n == 1:
        return False
    if n == 2:
        return True
    if n == 3:
        return True
    if n & 1:
        n_min = n - 1
        s = 0
        t = n_min
        while t & 1:
            s += 1
            t >>= 1
        for _ in range(k):
            a = random.randint(2, n_min - 1)
            if exp(a, n_min, n) != 1:
                return False
            for i in range(1, s + 1):
                twoi = exp(2, i)
                temp1 = exp(a, twoi * t, n)
                temp2 = exp(a, twoi >> 1 * t, n)
                if temp1 == 1 and (temp2 != 1 and temp2 != n_min):
                    return False
        return True
    return False


def pi(n):
    '''
    Returns the approximate number of primes <= n
        n:  upper limit of sequence of numbers
    '''
    if n == 1:
        return 0
    return n / math.log(n)


def generate_prime(k):
    '''
    Generates a prime number which is k bits long, None if no such number was found.
        k:  Length of prime number in bits
    '''
    if k <= 1:
        raise TypeError('k must be greater than 1')
    twok = exp(2, k)
    lowerLim = twok >> 1
    upperLim = twok - 1
    ntrials = max(int(pi(upperLim - lowerLim)), 50)  # perform 50 trials minimum
    for _ in range(ntrials):
        n = random.randint(lowerLim, upperLim)
        if is_prime(n):
            return n
    return None


if __name__ == '__main__':
    try:
        k = int(sys.argv[1])
    except IndexError:
        raise Exception('argument k missing')
    except TypeError:
        raise TypeError('argument k must be an integer')
    prime = generate_prime(k)
    print(prime)
