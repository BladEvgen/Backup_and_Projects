import random
import time


def execution_time(function):
    """Wrapper to calculate execution time for a function"""

    def wrapper(*args, **kwargs):
        print(f"Имя Функции: {function.__name__}")
        start_time = time.perf_counter()
        result = function(*args, **kwargs)
        execution_time = time.perf_counter() - start_time
        print(f"Время выполнения: {execution_time:.7f} секунд")
        return result

    return wrapper


def binary_search(array, target):
    low = 0
    high = len(array) - 1

    while low <= high:
        mid = (low + high) // 2
        if array[mid] == target:
            return mid
        elif array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


@execution_time
def binary_sort(array):
    """Perform binary sort on the given array"""
    sorted_arr = []

    for num in array:
        index = binary_search(sorted_arr, num)
        if index == -1:
            sorted_arr.append(num)
        else:
            sorted_arr.insert(index, num)


@execution_time
def insertion_sort(array):
    """Perform insertion sort on the given array"""
    for step in range(1, len(array)):
        key = array[step]
        j = step - 1
        while j >= 0 and key < array[j]:
            array[j + 1] = array[j]
            j = j - 1
        array[j + 1] = key


@execution_time
def shell_sort(array, length):
    """Perform shell sort on the given array"""
    interval = length // 2
    while interval > 0:
        for i in range(interval, length):
            temp = array[i]
            j = i
            while j >= interval and array[j - interval] > temp:
                array[j] = array[j - interval]
                j -= interval
            array[j] = temp
        interval //= 2


@execution_time
def merge_sort(array):
    """Perform merge sort on the given array"""
    return merge_sort_recursive(array)


def merge_sort_recursive(array):
    if len(array) <= 1:
        return array

    mid = len(array) // 2
    left = array[:mid]
    right = array[mid:]

    left = merge_sort_recursive(left)
    right = merge_sort_recursive(right)


def merge(left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])

    return merged


@execution_time
def selection_sort(array):
    """Perform selection sort on the given array"""
    for i, _ in enumerate(array):
        min_idx = i
        for j in range(i + 1, len(array)):
            if array[min_idx] > array[j]:
                min_idx = j
        array[i], array[min_idx] = array[min_idx], array[i]


if __name__ == "__main__":
    random.seed(42)

    array = random.sample(range(0, 1000), 100)
    print(f"\n\nНе отсортированный массив \n{array}")
    sort_type = int(
        input(
            "Введите номер алгоритма сортировки\n"
            "1. Shell Sort\n"
            "2. Insert Sort\n"
            "3. Merge Sort\n"
            "4. Binary Sort\n"
            "5. Select Sort\n"
        )
    )
    match sort_type:
        case 1:
            shell_sort(array=array, length=len(array))
            print(f"Отсортированный массив: {array}")
        case 2:
            insertion_sort(array=array)
            print(f"Отсортированный массив: {array}")
        case 3:
            merge_sort(array=array)
            print(f"Отсортированный массив: {array}")
        case 4:
            binary_sort(array=array)
            print(f"Отсортированный массив: {array}")
        case 5:
            selection_sort(array=array)
            print(f"Отсортированный массив: {array}")
        case _:
            print("Oops something happened wrong")
