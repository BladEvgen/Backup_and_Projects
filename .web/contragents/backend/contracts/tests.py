from django.test import TestCase
import requests


def _url(link: str = "") -> str:
    base_url = "http://localhost:8000"
    if link:
        return f"{base_url}/{link.lstrip('/')}"
    return base_url


def handle_response(response: requests.Response):
    try:
        response.raise_for_status()
        data = response.json()
        print(
            f'\n\t\t\tFunction {response.request.method} contracts Worked Well\nData: {data["results"]["data"]}\nType: {type(data)}\nResponse status: {response.status_code}\n'
        )
    except requests.HTTPError as e:
        print(
            f"\n\nHTTP error occurred: {e}\n\t\tError in {response.request.method}_contracts\n\n"
        )
    except Exception as e:
        print(f"An error occurred for {response.request.method} contracts: {str(e)}")


def get_contracts_exists():
    try:
        response = requests.get(_url("api/contracts/"))
        handle_response(response)
    except Exception as e:
        print(f"An error occurred for get exists contracts: {str(e)}")


def post_contracts():
    try:
        data = {
            "agent": 2,
            "total": 555,
            "comment": "Test world",
        }
        files = {"file": open("E:\\Users\\Evgeniy Kozlov\\Desktop\\dest.pdf", "rb")}
        response = requests.post(_url("api/contracts/"), data=data, files=files)
        handle_response(response)
    except Exception as e:
        print(f"Error for post occurred: {str(e)}")


if __name__ == "__main__":
    get_contracts_exists()
    post_contracts()
