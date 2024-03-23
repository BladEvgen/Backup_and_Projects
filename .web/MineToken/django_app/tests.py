from django.test import TestCase
import requests

API_URL = "http://localhost:8000/api/"


def make_request(method, endpoint, data=None):
    url = API_URL + endpoint
    try:
        response = requests.request(method, url, data=data)
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


def run_tests():
    try:
        response = make_request("GET", "user/list/")
        print("Response:", response, response.status_code)
        print("Response body:", response.json())
        if response.status_code not in [201, 200]:
            raise Exception("123")
    except:
        print("УСПЕХ")

    try:
        data = {"username": "Evgen_32", "password": "Qwertyu123!"}
        response = make_request("POST", "token/", data=data)
        print("Response:", response, response.status_code)
        print("Response body:", response.json())
        if response.status_code not in [201, 200]:
            raise Exception("123")
    except:
        print("Успех token на не правильного")

    token = ""
    try:
        data = {"username": "Evgen_3", "password": "Qwertyu123!"}
        response = make_request("POST", "token/", data=data)
        print("Response:", response, response.status_code)
        print("Response body:", response.json())
        if response.status_code not in [201, 200]:
            raise Exception("123")
        token = response.json()["token"]
        print("Успех в отсутсвии ошибки token на правильного")
    except:
        print("не успех")

    try:
        response = make_request("GET", f"token/check/?token={token}")
        print("Response:", response, response.status_code)
        if response.status_code in [201, 200]:
            print("Успешно check")
    except:
        print("Ошибка check")

    try:
        response = make_request("GET", f"user/list/?token={token}")
        print("Response:", response, response.status_code)
        print("Response body:", response.json())
        if response.status_code not in [201, 200]:
            raise Exception("123")
        print("УСПЕХ list")
    except:
        print("Не УСПЕХ list")

    try:
        data = {"token": token}
        response = make_request("POST", "token/block/", data=data)
        print("Response:", response, response.status_code)
        print("Response body:", response.json())
        if response.status_code not in [201, 200]:
            raise Exception("123")
        print("TOKEN BLOCKED УСПЕХ")
    except:
        print("НЕ УСПЕх TOKEN BLOCKED ")

    try:
        response = make_request("GET", f"user/list/?token={token}")
        print("Response:", response, response.status_code)
        print("Response body:", response.json())
        if response.status_code not in [201, 200]:
            raise Exception("123")
        print("УСПЕХ list")
    except:
        print("Не УСПЕХ list")


if __name__ == "__main__":
    run_tests()
