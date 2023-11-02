import asyncio
import sys
import time
from concurrent.futures import ThreadPoolExecutor


async def test_async():
    await asyncio.sleep(3)
    return True


def threading_test():
    time.sleep(3)
    return "второй поток"


def my_derocator(func):
    def wrapper(*args, **kwargs):
        if len(kwargs["login"]) > 0 and len(kwargs["password"]) > 0:
            return func(*args, **kwargs)

        raise "Одно из Полей пустые"

    return wrapper


@my_derocator
def check_user(login, password):
    return "Регистрация успешна"


def questions():
    # 1. В чем разница между списком и кортежем?
    # 3. Как развернуть список?
    # 4. Как работает умножение строк?
    # 5. Как работает умножение списка?
    # 7. Как округлить число до трех десятичных знаков?
    # 8. Как проверить, существует ли значение в списке?
    # 12. Получите список ключей из словаря
    # 13. Как перевести строку в верхний/нижний регистр?
    # 16. Как запросить у пользователя ввод
    # 17. Строка — это последовательность или нет?
    # 18. Что такое PEP
    # 20. Можно ли число сделать строкой и как
    # 24. Как пишутся комментарии в python
    # 25. Расскажите про арифметические операторы
    # 27. Как получить доступ к значениям в словаре?
    # 32. Что нужно сделать, чтобы функция возвратила значение?
    # 34. Как получить текущий рабочий каталог с помощью Python?
    # 37. Что такое декоратор?
    # 41. Виды типизации
    # 43. Как избежать конфликтов при импорте файлов
    # 45. Что означает self в классе?
    # 46. Назовите изменяемые и неизменяемые объекты
    # 72. Какой тип данных может быть значением в словаре и почему
    # 76. Напишите лучший код для перестановки двух чисел местами.

    # my_list_1 = [1, 2, 3, 4]
    # my_tuple_1 = (1, 2, 3, 4)

    # print(sys.getsizeof(my_list_1))
    # print(sys.getsizeof(my_tuple_1))

    # print(list(reversed(my_list_1)))
    # print(my_list_1[::-1])
    # my_list_2 = []

    # for i in my_list_1:
    #     my_list_2.insert(0, i)

    # print(my_list_2)

    # str1 = "Hello world"
    # str2 = "123"

    # print(f"{str1}, {str2}")
    # my_list_2 = [3, 4, 5, 6]  # создаем лист 2 с элементами

    # my_list_3 = [*my_list_1, *my_list_2]
    # print(my_list_3)

    # float1 = 8.14359

    # print(round(float1, 3))

    # value = 2
    # if value in my_list_1:
    #     print("Hello")
    # c = True if my_list_1.index(1) >= 0 else False

    # print(c)
    # # print(my_list_1.index(3))

    # my_dict = {"a": 1, "b": 2, "c": 3}

    # # print(my_dict.keys())

    # for keys, value in my_dict.items():
    #     print(keys, value)

    # # как вернуть из асинхронной
    # # как вернуть значение из второго потока

    # # result = await test_async()
    # # print(result)

    # with ThreadPoolExecutor(max_workers=1) as executor:
    #     future = executor.submit(threading_test)
    #     reusl = future.result()

    # resul_from_first = "Первое значени"
    # print(resul_from_first, reusl)

    # # login = input("Please enter login ")
    # # password = input("Please enter password ")

    # # check_user(login=login, password=password)

    # float1:str = "123"
    # print(float1)
    # float1 = 10
    # print(float1)
    pass

if __name__ == "__main__":
    # asyncio.run(questions())
    
    questions()