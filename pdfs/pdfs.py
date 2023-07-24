def plus_two(number: float | int, static_dig=2) -> int | float:
    try:
        return static_dig + number
    except TypeError as e:
        return e
    except Exception as e:
        return e


def arr_index(arr: list[int | float], index=0):
    try:
        element = arr[index]
        return element
    except IndexError as e:
        return e


def main():
    print(plus_two(number=5, static_dig="da"))  # print can only concatenate str (not "int") to str
    print(plus_two(number=5))  # will works okay
    my_array = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    print("\n<========================>\n")
    print(arr_index(my_array, 12))  # print list index out of range
    print(arr_index(my_array, 5))  # will works okay


if __name__ == "__main__":
    main()
