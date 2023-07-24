def find_min_cake_pieces(a: int, b: int) -> int:
    temp = a
    while True:
        if temp % b == 0:
            return temp
        temp += a


a = int(input("Введите число биологов в команде: "))
b = int(input("Введите число информатов в команде: "))

print(f"Наименьшее число которое делится на {a} и {b} без остатка, это {find_min_cake_pieces(a, b)}")