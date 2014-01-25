series = range(1, 101)

total_square = square_sum = 0

for n in series:
    total_square += n ** 2
    square_sum += n

print(square_sum**2 - total_square)
