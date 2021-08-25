from random import randint

class MillerRabin:
    def witness(a,n):
        t, u = 0, n-1
        while not (u&1):
            u >>= 1
            t += 1

        xp = 1
        xi = pow(a,u,n)
        for i in range(t):
            xp = xi
            xi = pow(xi,2, n)
            if xi == 1 and not(xp == 1 or xp == n-1):
                return True
        return xi != 1

    N = 10**6  # speedup: check if divisible by any of the primes < 10*5
    primes = []
    sieve = [True for i in range(N)]
    sieve[0] = sieve[1] = False
    for p in range(2, N):
        if sieve[p]:
            primes.append(p)
            for k in range(p*p,N,p):
                sieve[k] = False

    def is_prime(n, k=60):
        if n <= 1:
            return False
        if n == 2:
            return True
        if any(n % p == 0 for p in MillerRabin.primes):
            return False

        for i in range(k):
            a = 0
            while a == 0:
                x = randint(MillerRabin.N, n)
                a = x % n

            if MillerRabin.witness(a, n):
                return False

        return True

    def next_prime(n):
        ctr = 0
        while not MillerRabin.is_prime(n):
            n += 1

            ctr += 1
            if ctr % 10**3 == 0:
                print(f'{ctr} tested so far...')

        return n

def primeify(grid, w, h):
    colors = {}
    order = [1, 0, 2, 3, 4, 5, 6, 7, 8, 9] # can't have top left (first digit) be 0
    for pixel in grid:
        if pixel not in colors:
            assert(len(colors) < 10)
            colors[pixel] = str(order[len(colors)])

    n = int(''.join(colors[pixel] for pixel in grid))
    return [d for d in str(MillerRabin.next_prime(n))], colors
