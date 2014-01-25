primes = range(2, 105000)
for x in primes:
    n = x
    while x*n <= max(primes):
        if x*n in primes:
            primes.remove(x*n)
        n += 1

print(primes[10000])
