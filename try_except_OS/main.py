import os
import re


def is_valid(question: str, pattern: str) -> str:
    """that function checks by question and pattern is valid or not

    Args:
        question (str): Ask question and check by pattern
        pattern (str): give pattern to match

    Returns:
        str: return checked by pattern argument
    """
    while True:
        check = input(question)
        if re.match(pattern, check):
            return check
        print("Try again")


def main():
    path = r"./check/"
    login = is_valid(
        question="Enter your email: ",
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-z0-9-.]+$",
    )
    password = is_valid(
        question="Enter your password: ",
        pattern=r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$",
    )
    try:
        os.makedirs(path, exist_ok=True)
        if login and password:
            print("Valid")

            with open(
                f"{os.path.join(path)}credentials.txt", "a", encoding="utf-8"
            ) as file:
                file.write(f"Email: {login}\n")
                file.write(f"Password: {password}\n\n")

    except OSError as error:
        print(f"Error creating folder: {error}")
    except Exception as error:
        print(f"some error occurred: {error}")


if __name__ == "__main__":
    main()
