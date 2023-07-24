def superset(set_1, set_2):
    if set_1 == set_2:
        return "Множества равны"
    elif set_1 > set_2:
        return f"Объект {set_1} является чистым супермножеством"
    elif set_1 < set_2:
        return f"Объект {set_2} является чистым супермножеством"
    else:
        return "Супермножеств не обнаружено"


def set_gen(array: list[int]) -> set[int]:
    i = 0
    while i < len(array):
        counter = array.count(array[i])
        if counter > 1:
            array[i] = str(array[i]) * counter
        i += 1
    return set(array)


def add_word(dictionary):
    try:
        eng_word = input("Введите английское слово: ")
        fra_word = input("Введите перевод на французский: ")
        dictionary[eng_word] = fra_word
        print("Слово успешно добавлено в словарь.")
    except Exception as e:
        print("Произошла ошибка при добавлении слова:", str(e))


def remove_word(dictionary):
    try:
        eng_word = input("Введите английское слово для удаления: ")
        del dictionary[eng_word]
        print("Слово успешно удалено из словаря.")
    except KeyError:
        print("Слово не найдено в словаре.")
    except Exception as e:
        print("Произошла ошибка при удалении слова:", str(e))


def search_word(dictionary):
    try:
        eng_word = input("Введите английское слово для поиска: ")
        if eng_word in dictionary:
            print("Перевод на французский:", dictionary[eng_word])
        else:
            print("Слово не найдено в словаре.")
    except Exception as e:
        print("Произошла ошибка при поиске слова:", str(e))


def replace_word(dictionary):
    try:
        eng_word = input("Введите английское слово для замены: ")
        if eng_word in dictionary:
            fra_word = input("Введите новый перевод на французский: ")
            dictionary[eng_word] = fra_word
            print("Слово успешно заменено.")
        else:
            print("Слово не найдено в словаре.")
    except Exception as e:
        print("Произошла ошибка при замене слова:", str(e))


def eng_french():
    dictionary = {}
    while True:
        print(
            "\nМеню:\n1. Добавить слово\n2. Удалить слово\n3. Найти слово\n4. Заменить слово\n5. Выйти"
        )
        choice = input("Выберите действие (1-5): ")
        match choice:
            case "1":
                add_word(dictionary)
            case "2":
                remove_word(dictionary)
            case "3":
                search_word(dictionary)
            case "4":
                replace_word(dictionary)
            case "5":
                break
            case _:
                print("Пожалуйста, выберите действие из списка.")


def caesar_cipher(text: str, shift: int) -> str:
    encrypted_text = ""
    for char in text:
        if char == " ":
            encrypted_text += " "
        else:
            encrypted_char = chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
            encrypted_text += encrypted_char
    return encrypted_text


def count_fruits_1(fruit: str, fruit_tuple: tuple[str]) -> int:
    count = 0
    for item in fruit_tuple:
        if item == fruit:
            count += 1
    return count


def count_fruits_2(fruit: str, fruit_tuple: tuple[str]) -> int:
    count = 0
    for item in fruit_tuple:
        if fruit in item:
            count += 1
    return count


def manufacturer_replace(manufacturer, old_manufacturer, new_manufacturer):
    try:
        manufacturer = list(manufacturer)
        for i in range(len(manufacturer)):
            if manufacturer[i] == old_manufacturer:
                manufacturer[i] = new_manufacturer
        return tuple(manufacturer)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        return manufacturer


def main():
    print("\n\n======================\n\n")
    print(superset({1, 5, 3, 6}, {3, 7}))
    print(superset({1, 5, 3, 6}, {6, 3, 1, 5}))

    print(set_gen([4, 4, 1, 2, 4]))
    print(set_gen([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]))

    print("\n\n=========Шифр Цезаря=========\n\n")
    print(
        f'Шифр Цезаря: {caesar_cipher(text = input("Введите желаемый текст для шифрования (на английском): ").lower(), shift = int(input("Введите сдвиг для шифровки: ")))}'
    )

    print("\n\n=========Фрукт в кортеже v1=========\n\n")
    try:
        fruit_tuple = (
            "apple",
            "orange",
            "banana",
            "pineapple",
            "banana",
            "apple",
            "banana",
            "banana",
        )  # banana 4
        fruit = input("Введите название фрукта: ")
        print(
            f"Количество {fruit} в кортеже {fruit_tuple}: {count_fruits_1(fruit, fruit_tuple)} раз (-а)"
        )
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    print("\n\n=========Фрукт в кортеже v2=========\n\n")
    try:
        fruit_tuple = (
            "banana",
            "apple",
            "bananamango",
            "mango",
            "strawberry-banana",
        )  # banana 3
        fruit = input("Введите название фрукта: ")
        print(
            f"Количество {fruit} в кортеже {fruit_tuple}: {count_fruits_2(fruit, fruit_tuple)} раз (-а)"
        )
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    print("\n\n=========Производитель машин=========\n\n")
    manufacturers = ("BMW", "Mercedes", "Audi", "BMW", "Toyota", "Honda", "KIA", "BMW")
    print(f"Старый кортеж производителей: {manufacturers}")
    print(
        f"Обновленный кортеж производителей автомобилей: {manufacturer_replace(manufacturer = manufacturers, old_manufacturer = input('Введите название производителя для замены: '), new_manufacturer = input('Ввдетие слово для замены: '))}"
    )
    print("\n\n=========СЛОВАРЬ=========\n\n")
    eng_french()


if __name__ == "__main__":
    main()
