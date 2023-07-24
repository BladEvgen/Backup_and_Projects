def find_missing_card():
    n = int(input("Число N: "))
    sum = n * (n + 1) // 2

    for i in range(n - 1):
        card = int(input(f"Введите номер {i+1} карты: "))
        sum -= card
    return sum


print(f"Номер потерянной карты: {find_missing_card()}")


def squares_of_natural():
    squares = []
    n = int(input("Введите границу по которой нужно найти квадраты натуральных чисел: "))
    i = 1
    while i * i <= n:
        squares.append(i * i)
        i += 1
    return squares


print(f"Output: {squares_of_natural()}")