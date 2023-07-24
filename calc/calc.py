from math import sqrt, pow


def multiply(a: int | float, b: int | float) -> int | float:
    return a * b


def divide(a: int | float, b: int | float) -> float | None:
    if b != 0:
        return a / b
    else:
        print("Error division by zero")
        return None


def plus(a: int | float, b: int | float) -> int | float:
    return a + b


def minus(a: int | float, b: int | float) -> int | float:
    return a - b


def main():
    action = input(
        "Enter action (symbol): "
        "\n1) * (multiply)"
        "\n2) / (divide)"
        "\n3) + (add)"
        "\n4) - (subtract)"
        "\n5) power"
        "\n6) sqrt\n"
    )
    if action == "sqrt":
        a = float(input("Enter a: "))
        print(sqrt(a))
    else:
        a = float(input("Enter a: "))
        b = float(input("Enter b: "))
    match action:
        case "*":
            print("a digit multiplied by b digit")
            print(multiply(a, b))
        case "/":
            print("a digit divide by b digit")
            print(divide(a, b))
        case "+":
            print(plus(a, b))
        case "-":
            print(minus(a, b))
        case "power":
            print("a digit raised to b digit")
            print(pow(a, b))
        case _:
            print("Invalid action")


if __name__ == "__main__":
    main()
