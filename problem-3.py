num = 600851475143

primes = list(range(2, 10000))
for x in primes:
    n = x
    while x*n <= max(primes):
        if x*n in primes:
            primes.remove(x*n)
        n += 1

final_numbers = []

for n in primes:
    if n > num:
        break
    if (num % n) > 0:
        continue
    else:
        final_numbers.append(n)

print(final_numbers)
