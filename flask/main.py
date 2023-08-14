"""My first Flask application"""
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
    """View class for Flask application"""

    class Base:
        """Base class for Flask views"""

        @staticmethod
        @app.route("/")
        def home():
            """display homepage in carousel view

            Returns:
                render_template: home
            """
            query_str = "SELECT title, description, image FROM services"
            carousel_items = Database.query(query_str)
            return render_template(
                template_name_or_list="home.html", carousel_items=carousel_items
            )

        @staticmethod
        @app.route("/about")
        def about():
            """Displays about page

            Returns:
                render_template: about
            """
            return render_template(template_name_or_list="about.html")

        @staticmethod
        @app.route("/faqs")
        def faqs():
            """Display FAQs

            Returns:
                render_template: faqs
            """
            return render_template(template_name_or_list="faqs.html")

    class Logic:
        """Full logic of application will be executed here"""

        @staticmethod
        @app.route("/services")
        def services():
            """that function display information about services on the page

            Returns:
                rendered HTML page: with sql query and current date.
            """
            query_str = "SELECT id, title, price_low, price_high, description, image FROM services"
            services = Database.query(query_str)
            date = datetime.datetime.now().strftime("%d %b")
            return render_template(
                template_name_or_list="services.html", services=services, date=date
            )

        @staticmethod
        @app.route("/service/<int:service_id>")
        def service_details(service_id: int):
            """that function display information about exactly one service details on the page

            Args:
                service_id (int): will search for specific service_id
                in database and display information about it:
                title,
                price_low,
                price_high,
                description,
                image.

            Returns:
                rendered HTML page: with information about service_id
            """
            query_str = """SELECT id, title, price_low, price_high, description, image
            FROM services WHERE id = ?"""
            service = Database.query(query_str, (service_id,), many=False)

            if service:
                return render_template("service_details.html", service=service)
            else:
                return "Service not found.", 404


class Database:
    """Database class for connecting to the database"""

    @staticmethod
    def query(query_str: str, args=(), many=True) -> list | None:
        """Connect to the database

        Args:
            query_str (str): Sql query string
            args (tuple, optional): using for escape from sql injections. Defaults to ().
            many (bool, optional): if you want to return all from db use many=True,
            otherwise set False for one row. Defaults to True.

        Returns:
            list | None
        """
        local_path = os.path.join(os.path.dirname(__file__), "db")
        os.makedirs(local_path, exist_ok=True)
        with sqlite3.connect(f"{local_path}/database.db") as connection:
            cursor = connection.cursor()
            cursor.execute(query_str, args)
            try:
                if many:
                    return cursor.fetchall()
                return cursor.fetchone()
            except sqlite3.Error as error:
                print(f"Error with sqlite3 connection {error}")
                return None
            except Exception as error:
                print(f"Oop something went wrong {error}")
                return None


class DatabaseTools:
    """that class needs to be used when you want to work with database"""

    @staticmethod
    def create_db():
        """create a new database
        with id,
        title,
        price_low,
        price_high,
        description,
        image"""
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
        """drop the database"""
        Database.query("DROP TABLE IF EXISTS services")

    @staticmethod
    def insert_service(
        title: str,
        price_low: int | float,
        price_high: int | float,
        description: str,
        image=None,
    ):
        """insert service into database

        Args:
            title (str): title of service
            price_low (int | float): lower price of the service
            price_high (int | float): higher price of the service
            description (str): description for that service
            image (_type_, optional): url or path to image. Defaults to None.
        """
        query_str = """
        INSERT INTO services (title, price_low, price_high, description, image)
        VALUES (?, ?, ?, ?, ?)
        """

        service_data = (title, price_low, price_high, description, image)

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
        """This function is used to update a service by its id in the database

        Args:
            service_id (int): item id of the service which will be updated
            title (str): new title of the service
            price_low (int | float): lower price of the service
            price_high (int | float): higher price of the service
            description (str): description for that exactly service
            image (_type_, optional): url to image Defaults to None.
        """
        query_str = """
        UPDATE services
        SET title = ?, price_low = ?, price_high = ?, description = ?, image = ?
        WHERE id = ?
        """
        service_data = (title, price_low, price_high, description, image, service_id)

        Database.query(query_str, service_data)


if __name__ == "__main__":
    app.run(debug=True)
