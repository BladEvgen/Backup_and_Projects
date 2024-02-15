import json
import random
import datetime
import requests


def load_config():
    with open("config.json", "r") as f:
        config = json.load(f)
    return config


def generate_random_data(num_entries):
    data_list = []
    current_time = datetime.datetime.now()
    for _ in range(num_entries):
        random_device_time = (
            current_time
            - datetime.timedelta(hours=random.randint(0, 2))
            + datetime.timedelta(hours=random.randint(0, 1))
        )
        data = {
            "serial_id": f"DEVICE_{random.randint(1, 1000)}",
            "x": round(random.uniform(-90, 90), 6),
            "y": round(random.uniform(-180, 180), 6),
            "is_working": random.choice([True, False]),
            "fuel": random.randint(0, 100),
            "speed": random.randint(0, 100),
            "device_time": random_device_time.strftime("%Y-%m-%d %H:%M:%S"),
        }
        data_list.append(data)
    return {"message": data_list}


def send_data_to_server(data):
    config = load_config()
    ip = config.get("ip", "127.0.0.1")
    port = config.get("port", 8000)
    url = f"http://{ip}:{port}/api/get_params/"
    response = requests.post(url, json=data)
    if response.status_code in (200, 201):
        print("Data sent successfully.")
    else:
        print(f"Failed to send data. Status code: {response.status_code}")


if __name__ == "__main__":
    random_data = generate_random_data(3)
    print(json.dumps(random_data, indent=4))  # Debug print for manually check api
    send_data_to_server(random_data)
