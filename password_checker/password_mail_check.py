import requests
import json
import os
import re


def get_even_json():
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts")
        data = response.json()
        even_posts = [post for post in data if post["id"] % 2 == 0]
        file_path = os.path.join(os.path.dirname(__file__), "even.json")
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(even_posts, file, indent=4)
    except requests.exceptions.RequestException as e:
        print("Error occurred while making the request:", e)
    except json.JSONDecoderError as e:
        print("Error occurred while decoding the JSON:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


def email_check(email: str) -> bool:
    return True if re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-z0-9-.]+$", email) is not None else False


def password_check(password: str) -> bool:
    return True if re.match(r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password) is not None else False


def user_registration():
    email = input("Введите email: ")
    password = input("Введите пароль: ")

    if email_check(email) and password_check(password):
        print("Регистрация прошла успешно!")
    else:
        print("Некорректный email или пароль. Повторите попытку.")
        user_registration()


def main():
    get_even_json()
    # print(email_check("example@mail.com"))
    # print(password_check("Qwerty123!"))    
    user_registration()


if __name__ == "__main__":
    main()
