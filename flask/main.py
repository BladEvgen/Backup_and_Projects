import datetime
import os
import sqlite3
from flask import Flask, render_template

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="templates",
)



class View:
    class Base:
        @staticmethod
        @app.route("/")
        def home():
            query_str = "SELECT title, description, image FROM services"
            carousel_items = Database.query(query_str)
            return render_template(template_name_or_list="home.html", carousel_items=carousel_items)

        @staticmethod
        @app.route("/about")
        def about():
            return render_template(template_name_or_list="about.html")

        @staticmethod
        @app.route("/faqs")
        def faqs():
            return render_template(template_name_or_list="faqs.html")

    class Logic:
        @staticmethod
        @app.route("/services")
        def services():
            query_str = "SELECT id, title, price_low, price_high, description, image FROM services"
            services = Database.query(query_str)
            date = datetime.datetime.now().strftime("%d %b")
            return render_template(
                template_name_or_list="services.html", services=services, date=date
            )

        @staticmethod
        @app.route("/service/<int:service_id>")
        def service_details(service_id):
            query_str = "SELECT id, title, price_low, price_high, description, image FROM services WHERE id = ?"
            service = Database.query(query_str, (service_id,), many=False)

            if service:
                return render_template("service_details.html", service=service)
            else:
                return "Service not found.", 404


class Database:
    @staticmethod
    def query(query_str: str, args=(), many=True) -> list | None:
        local_path = os.path.join(os.path.dirname(__file__), "db")
        os.makedirs(local_path, exist_ok=True)
        with sqlite3.connect(f"{local_path}/database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(query_str, args)
            try:
                if many:
                    return cursor.fetchall()
                return cursor.fetchone()
            except Exception as error:
                return None


class DatabaseTools:
    @staticmethod
    def create_db():
        Database.query(
            """
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                price_low REAL NOT NULL,
                price_high REAL NOT NULL,
                description TEXT NOT NULL,
                image TEXT
            )
            """
        )

    @staticmethod
    def drop_db():
        Database.query("DROP TABLE IF EXISTS services")

    @staticmethod
    def insert_service(
        title: str,
        price_low: int | float,
        price_high: int | float,
        description: str,
        image=None,
    ):
        query_str = """
        INSERT INTO services (title, price_low, price_high, description, image)
        VALUES (:title, :price_low, :price_high, :description, :image)
        """

        service_data = {
            "title": title,
            "price_low": price_low,
            "price_high": price_high,
            "description": description,
            "image": image,
        }

        Database.query(query_str, service_data)

    @staticmethod
    def update_service_by_id(
        service_id: int,
        title: str,
        price_low: int | float,
        price_high: int | float,
        description: str,
        image=None,
    ):
        query_str = """
        UPDATE services
        SET title = :title, price_low = :price_low, price_high = :price_high, description = :description, image = :image
        WHERE id = :service_id
        """
        service_data = {
            "service_id": service_id,
            "title": title,
            "price_low": price_low,
            "price_high": price_high,
            "description": description,
            "image": image,
        }

        Database.query(query_str, service_data)


if __name__ == "__main__":
    app.run(debug=True)
