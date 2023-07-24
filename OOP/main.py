from dotenv import load_dotenv
import os
import sqlite3
import telebot


class DataBase:
    @staticmethod
    def execute_query_to_sqlite(
        query: str, args=(), many=True, silent_error=True
    ) -> any:
        try:
            with sqlite3.connect("db/database.db") as connection:
                cursor = connection.cursor()
                cursor.execute(query, args)
                if many:
                    return cursor.fetchall()
                return cursor.fetchone()
        except Exception as error:
            print(error)
            if silent_error is False:
                raise Exception(error)
            return None

    @staticmethod
    def create_tickets_table():
        DataBase.execute_query_to_sqlite(
            query="""CREATE TABLE IF NOT EXISTS tickets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  destination TEXT NOT NULL,
                  departure_date TEXT NOT NULL,
                  price REAL NOT NULL)"""
        )

    @staticmethod
    def insert_tickets(destination: str, departure_date, price: float | int):
        DataBase.execute_query_to_sqlite(
            query="""
                  INSERT INTO tickets (destination, departure_date, price)
                  VALUES (?, ?, ?)
                  """,
            args=(destination, departure_date, price),
        )

    @staticmethod
    def get_all_tickets() -> list[tuple] | None:
        data = DataBase.execute_query_to_sqlite(
            query="""
                  SELECT id, destination, departure_date, price 
                  FROM tickets 
                  ORDER BY price DESC
                  """
        )
        return data


def main():
    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    API_TOKEN = os.getenv("API_TOKEN")

    if not API_TOKEN:
        raise Exception("API_TOKEN is not defined in the environment variables.")

    bot = telebot.TeleBot(API_TOKEN)
    DataBase.create_tickets_table()

    # tickets_data = [
    #     ("Peru", "2023-07-06", 299.9),
    #     ("Beijin", "2023-08-15", 0.0001),
    #     ("Astana", "2023-07-21", 666.6),
    # ]
    # for ticket in tickets_data:
    #     DataBase.insert_tickets(*ticket)

    @bot.message_handler(commands=["start"])
    def send_welcome(message):
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
        register_button = telebot.types.KeyboardButton("/register")
        tickets_button = telebot.types.KeyboardButton("/tickets")
        markup.add(register_button, tickets_button)

        bot.reply_to(
            message, "Добро пожаловать в бот регистрации билетов!", reply_markup=markup
        )

    @bot.message_handler(commands=["register"])
    def register_ticket(message):
        msg = bot.reply_to(
            message,
            "Пожалуйста, введите данные о билете в следующем формате:\nМесто назначения, Дата вылета, Цена\nПример: <b><i>Алматы, 2024-01-01, 999.99</i></b>",
            parse_mode="HTML",
        )
        bot.register_next_step_handler(msg, process_ticket_registration)

    def process_ticket_registration(message):
        try:
            ticket_details = message.text.split(",")
            destination = ticket_details[0].strip()
            departure_date = ticket_details[1].strip()
            price = float(ticket_details[2].strip())

            DataBase.insert_tickets(destination, departure_date, price)
            bot.reply_to(message, "Билет успешно зарегистрирован!")
        except (IndexError, ValueError):
            bot.reply_to(
                message, "Неверные данные о билете. Пожалуйста, попробуйте еще раз."
            )

    @bot.message_handler(commands=["tickets"])
    def show_all_tickets(message):
        tickets = DataBase.get_all_tickets()
        if tickets:
            ticket_list = "\n".join(
                [
                    f"<b>Место назначения: {ticket[1]}</b>\n<i>Дата вылета: {ticket[2]}</i>\nЦена: {ticket[3]}"
                    for ticket in tickets
                ]
            )
            bot.reply_to(
                message, f"Зарегистрированные билеты:\n{ticket_list}", parse_mode="HTML"
            )
        else:
            bot.reply_to(message, "Билеты не найдены.")

    bot.polling()


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
    # https://t.me/bladstep_bot
