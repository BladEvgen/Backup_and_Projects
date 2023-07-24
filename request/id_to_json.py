import json 
import requests
import os

n = int(input('Enter a number for the request: '))

url = f"https://jsonplaceholder.typicode.com/todos/{n}"
try:
    response = requests.get(url)
    response.raise_for_status()

    todo = response.json()

    file_path = os.path.join(os.path.dirname(__file__), "json", f"{todo['id']}.json")

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(todo, file, indent=4)

    print("Todo item saved successfully.")
except requests.exceptions.RequestException as e:
    print("Error occurred while making the request:", e)
except json.JSONDecodeError as e:
    print("Error occurred while decoding the JSON response:", e)
except Exception as e:
    print("An unexpected error occurred:", e)
