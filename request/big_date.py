import json
import os
from datetime import datetime, timedelta


def get_valid_datetime(prompt):
    while True:
        try:
            date_str = input(prompt)
            date = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
            return date
        except ValueError:
            print("Неверный формат даты. Введите в формате dd.mm.yyyy HH:MM:SS.")


def calculate_time_left(dt1, dt2):
    time_difference = abs(dt2 - dt1)
    days = time_difference.days
    seconds = time_difference.seconds
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    time_left = f"{days} дней(-день), {hours} час(-ов), {minutes} минут(-а/-ы), {seconds} секунд(-а/-ы)"
    return time_left


def save_dates_to_json(result):
    directory = os.path.join(os.path.dirname(__file__), "json")
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, "dates.json")
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(result, file, ensure_ascii=False)
    print("Даты сохранены в ", file_path)


def main():
    date1 = get_valid_datetime("Введите первую дату и время (dd.mm.yyyy HH:MM:SS): ")
    date2 = get_valid_datetime("Введите вторую дату и время (dd.mm.yyyy HH:MM:SS): ")

    time_left = calculate_time_left(date1, date2)

    largest_date = max(date1, date2).strftime("%d.%m.%Y %H:%M:%S")
    smallest_date = min(date1, date2).strftime("%d.%m.%Y %H:%M:%S")

    result = {
        "largest_date": largest_date,
        "smallest_date": smallest_date,
        "time_left": time_left,
    }

    save_dates_to_json(result)

    print("Время, оставшееся до большей даты:", time_left)


if __name__ == "__main__":
    main()
