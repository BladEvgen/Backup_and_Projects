import os
import psycopg2
from dotenv import load_dotenv
from contextlib import closing

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def read_data_from_file_and_send_to_db(file_path, table_name):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()[1:]

        with closing(
            psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
            )
        ) as conn:
            with conn.cursor() as cur:
                for line in lines:
                    data = line.strip().split(",")
                    item = {
                        "datetime": data[0],
                        "name": data[1],
                        "age": int(data[2]),
                        "is_employed": data[3] == "TRUE",
                    }
                    cur.execute(
                        "INSERT INTO {} (datetime, name, age, is_employed) VALUES (%s, %s, %s, %s)".format(
                            table_name
                        ),
                        (
                            item["datetime"],
                            item["name"],
                            item["age"],
                            item["is_employed"],
                        ),
                    )

                conn.commit()

        print("Данные успешно отправлены в базу данных.")
    except Exception as e:
        print("Произошла ошибка:", e)


def read_data_from_db_and_write_to_file(table_name, file_path):
    try:
        with closing(
            psycopg2.connect(
                host=os.getenv("DB_HOST"),
                port=os.getenv("DB_PORT"),
                dbname=os.getenv("DB_NAME"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
            )
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT datetime, name, age, is_employed FROM {}".format(table_name)
                )
                data = cur.fetchall()

        with open(file_path, "w") as file:
            column_names = ["datetime", "name", "age", "is_employed"]
            file.write(",".join(column_names) + "\n")
            for item in data:
                row = ",".join(str(value) for value in item)
                file.write(row + "\n")

        print("Данные успешно записаны в текстовый файл.")
    except Exception as e:
        print("Произошла ошибка:", e)


if __name__ == "__main__":
    read_data_from_file_and_send_to_db("input.txt", "users_table")
    read_data_from_db_and_write_to_file("users_table", "output.txt")
