def average_mark():
    scores = input("Введите список оценок через пробел: ").split()
    counts = [0, 0, 0, 0]
    for score in scores:
        if score == "5":
            counts[0] += 1
        if score == "4":
            counts[1] += 1
        if score == "3":
            counts[2] += 1
        if score == "2":
            counts[3] += 1

    count_str = " ".join(str(count) for count in counts)
    average = sum(int(score) for score in scores) / len(scores)

    count_output = f"подсчет оценок (пятерки, четверки, тройки, двойки): {count_str}"  # спросил у нейросети как вывести понятный принт
    average_output = f"средний балл {average}"
    return count_output, average_output


def replace_grades(grades):
    try:
        pass
        grades_list = grades.split()
        for i in range(len(grades_list)):
            if grades_list[i] == "2":
                grades_list[i] = "3"
        return " ".join(grades_list)
    except Exception as e:
        print(f"произошла ошибка {e}")
        return grades


def calculate_sum_of_squares():
    numbers = []
    sum_of_numbers = 0

    while sum_of_numbers != 0 or len(numbers) == 0:
        num = int(input())
        numbers.append(num)
        sum_of_numbers += num

    sum_of_squares = sum([x**2 for x in numbers])
    return sum_of_squares



print("\n\n=========Подсчет средней оценки Васи=========\n\n")
print(average_mark())

print("\n\n=========Изменение оценки Васи=========\n\n")
grades = input("Введите оценки через пробел: ")
print(f"Исходные оценки {grades}")
print(f"Обновленный оенки: {replace_grades(grades)}")


print("\n\n=========Суммирование элементов пока не 0=========\n\n")
print(calculate_sum_of_squares())
