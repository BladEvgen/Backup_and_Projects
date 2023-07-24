def search_target(array: list[float], target: float) -> bool:
    if not array:
        return False

    if array[0] == target:
        return True

    return search_target(array[1:], target)


nums_str = input("Введите элементы массива для проверки (через пробел): \n")
nums = [float(num) for num in nums_str.split()]

target = None

while target is None:
    target_input = input("Введите число для поиска: ")
    try:
        target = float(target_input)
    except:
        print("Неверный формат ввода. Пожалуйста, введите число.")


print(search_target(nums, target))
