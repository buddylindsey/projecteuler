number = 20
upper = 20

kill_it = True

while kill_it:
    number += upper

    for i in range(2, 20):
        if (number % i) > 0:
            break
        if (number % i) == 0 and i == (upper - 1):
            kill_it = False

print(number)
