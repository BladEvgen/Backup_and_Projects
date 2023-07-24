#задание 1 
side1 = int(input("Введите 1-ю сторону треугольника число: "))
side2 = int(input("Введите 2-ю сторону треугольника число: "))
side3 = int(input("Введите 3-ю сторону треугольника число: "))

if side1 + side2 > side3 and side2 + side3 > side1 and side1 + side3 > side2:
    print("True")
else:
    print("False")


#задание 2
chet = int(input('Введите целое число '))

if chet % 2 == 0:
	print('True')
else:
	print('False')


#задание 3
a = float(input("Введите число а "))
b = float(input("Введите число b "))
c = float(input("Введите число c "))


if a+b > c:
	print(f'{a} + {b} > {c} (true)')
elif a+b == c:
	print(f'{a} + {b} = {c}')
else:
	print(f'{a} + {b} < {c} (false)')



#задание 4

dig1 = int(input("Введите целое число 1 "))

dig2 = int(input("Введите целое число 2 "))

print(True if dig1 > dig2 else False)