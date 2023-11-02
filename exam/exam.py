import multiprocessing
import os
import sys
import re
import time
import json
import requests
from openpyxl import Workbook
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QPushButton,
    QTextEdit,
    QListWidget,
    QLabel,
)


def task_1():
    """
    1) Выведите в консоль 5 звёздочек, используя умножение строк.
    2) Напишите программу на Python, чтобы создать треугольник из звезд.
    """
    print("*" * 5)
    for i in range(1, 8):
        space = " " * (8 - i)
        stars = "*" * (2 * i - 1)
        print(space + stars)


def task_2():
    """
    [2 балла]
    1) Получите через http – запрос все объекты из jsonplaceholder todo.
    2) Запишите все полученные данные в новую папку temp, в разные .json файлы.
    3) Прочитайте все файлы из папки, и запишите данные каждого в единый .xlsx файл.
    """
    """
    Задание 2.
    [2 балла]
    1) Получите через http – запрос все объекты из jsonplaceholder todo.
    2) Запишите все полученные данные в новую папку temp, в разные .json файлы.
    3) Прочитайте все файлы из папки, и запишите данные каждого в единый .xlsx файл.
    """
    temp_dir = os.path.join(os.path.dirname(__file__), "temp")
    if not os.path.exists(temp_dir):
        os.mkdir(temp_dir)
    url = "https://jsonplaceholder.typicode.com/todos/"
    response = requests.get(url)
    data = response.json()

    for todo in data:
        filename = os.path.join(temp_dir, f"todo_{todo['id']}.json")
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(todo, f, indent=4)

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(["id", "title", "completed"])
    for todo in data:
        worksheet.append([todo["id"], todo["title"], todo["completed"]])
    workbook.save("todos.xlsx")


def task_3():
    """
    Задание 3.
    [2 балла]
    1) Напишите любой пример бесконечного таймера, через цикл while.
    2) Модифицируйте код, чтобы можно было задать множитель для секунд от ввода пользователя.
    """
    seconds = int(input("Введите seconds 0 для выхода "))
    multiplier = float(input("Введите multiplier  "))

    while True:
        if seconds == 0:
            break

        while seconds > 0:
            print(f"Осталось {seconds} секунд.")
            time.sleep(1 / multiplier)
            seconds -= 1
        print("Конец")


def task_4():
    """
    1) Определите класс car с двумя атрибутами: color и speed. Затем создайте экземпляр и верните speed.
    2) Модифицируйте код так, чтобы при старте программы, пользователь мог сам задать скорость машины, проверку выполните через регулярное выражение.
    """

    class Car:
        def __init__(self, color, speed):
            self.color = color
            self.speed = speed

    def valid_speed():
        while True:
            speed_input = input("Введите скорость машины: ")
            if re.match(r"^\d+(\.\d+)?$", speed_input):
                return float(speed_input)
            print("Введите корректное значение скорости")

    color = input("Введите цвет машины: ")
    speed = valid_speed()
    car = Car(color, speed)
    print(f"Скорость машины: {car.speed} км/ч\nЦвет машины {car.color}")


def task_5():
    """
    1) Реализуйте программу с интерфейсом на библиотеке pyqt6, необходимо чтобы при нажатии происходил запрос по адресу, введённому в textedit, статус запроса выводите в консоль.
    2) Модифицируйте код так, чтобы статус запроса с описанием выводился в текстовое поле в инстерфейсе. Соберите программу в исполняемый файл, т.е. .exe .
    """
    pass


class App(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Http APP")
        self.setGeometry(100, 100, 400, 200)

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.label = QLabel("Enter URL:", self)
        self.layout.addWidget(self.label)

        self.text_edit = QTextEdit(self)
        self.layout.addWidget(self.text_edit)

        self.status_label = QLabel("", self)
        self.layout.addWidget(self.status_label)

        self.status_text = QTextEdit(self)
        self.status_text.setReadOnly(True)
        self.layout.addWidget(self.status_text)

        self.request_button = QPushButton("Send request", self)
        self.request_button.clicked.connect(self.send_request)
        self.layout.addWidget(self.request_button)

    def send_request(self):
        self.status_label.setText("Response")

        url = self.text_edit.toPlainText()
        try:
            response = requests.get(url)
            status_code = response.status_code
            status_text = response.reason

            self.status_text.setText(
                f"Status code: {status_code}\nStatus Text: {status_text}\n"
            )
        except Exception as e:
            self.status_text.setText(f"Error: {str(e)}")
            self.status_label.setText(f"Error:")


def task_6(start: int = 1, end: int = 100000):
    """
    Задание 6.
    [4 балла]
    1) Подбор пароля для тестирования: записать в документ в один поток числа от 1 до 100000.
    2) Переписать логику на 10 мультипроцессов и в конце склейку в один.
    """
    with open("password.txt", "w") as file:
        for number in range(start, end + 1):
            file.write(str(number) + "\n")


def task_6_multi(number: int):
    with open("multi_password.txt", "a") as file:
        file.write(str(number))


def complex_task():
    """
    Комплексное задание:
    В качестве практической части экзамена выполните реализацию проекта, техническое задание которого описано ниже:

    Тема: Локальный веб-сайт с публикациями задач и настольный клиент к нему.
    Описание: Для реализации используйте pyqt6 и flask. Данные можно сохранять в текстовый, json или .sql файлы.
    Страницы: основная страница, где происходит вывод задач и форма для добавления новых
    Интерфейс: окно с выводом всех задач и текстовым полем с кнопкой для добавления новых

    Разрешено:
    • Смотреть код и реализацию функционала в своих старых проектах, частично брать оттуда код для изменения.
    • Смотреть реализацию функционала в интернете.
    • Реализовывать дополнительный функционал, ради увеличения баллов.

    Запрещено:
    • Брать код преподавателя с «репозиториев» или полностью копировать чужие проекты.


    Реализованно в отдельной папке complex
    """
    pass


def main():
    task_1()
    task_2()
    task_3()
    task_4()

    with multiprocessing.Pool() as pool:
        pool.map(task_6_multi, range(1, 100001))

    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
