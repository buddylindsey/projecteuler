set_one = set_two = range(100, 1000)

total_set = []

for i in set_one:
    for j in set_two:
        prod = str(i * j)
        part_one, part_two = prod[:len(prod)/2], prod[len(prod)/2:]

        if part_one == part_two[::-1]:
            total_set.append(prod)

print(max(sorted(total_set)))
