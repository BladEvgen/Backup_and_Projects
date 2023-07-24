def money_1(s: int | float, p: int | float, m: int | float) -> bool:
    total_money = s + p
    return True if total_money <= m else False


if money_1(500, 600, 2000):
    print("Да")
else:
    print("Нет")


def money_2(s_input, p_input, m_input):
    while True:
        if s_input.isdigit() and p_input.isdigit() and m_input.isdigit():
            s = int(s_input)
            p = int(p_input)
            m = int(m_input)
            break
        else:
            print("Ошибка! Введите числовые значения для всех полей.")

    total_money = s + p
    if total_money <= m:
        print("Да 1")
    elif m == total_money or total_money > m:
        print("да 2")
    else:
        print("Нет")


money_2(
    s_input=input("Введите стоимость онлайн кинотеатра: "),
    p_input=input("Введите стоимость пиццы: "),
    m_input=input("Введите зарплату: "),
)
