from functools import wraps
import sqlite3
import os
from django.http import JsonResponse
from datetime import datetime
from rest_framework.request import Request
from rest_framework.response import Response


class Utils:
    @staticmethod
    def get_database_path(database_filename, source_folder="database"):
        base_path = os.path.abspath(
            os.path.join("django_digital_home", "desktop", "src", source_folder)
        )
        return os.path.join(base_path, database_filename)

    @staticmethod
    def get_current_timestamp():
        return datetime.now()


class DRF:
    @staticmethod
    def decor_error(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _request: Request = args[0]
            try:
                _response: dict = func(*args, **kwargs)
                return Response(data=_response, status=200)
            except Exception as error:
                print(error)
                # TODO ЛОГИРОВАНИЕ
                return Response(data={"error": str(error)}, status=500)

        return wrapper


def auth_paramaterized_decorator(_token: str = ""):
    def decor(func):
        def wrapper(*args, **kwargs):
            received_token = args[0].headers.get("Authorization", "")
            print("Received Token:", received_token)  # Add this line for debugging

            if received_token != _token:
                return JsonResponse(
                    {"error": "Not valid token"}, status=401, safe=False
                )
            try:
                _response: dict = func(*args, **kwargs)
                return JsonResponse(data=_response, status=200, safe=False)
            except Exception as error:
                Sql.save_error_to_db(str(error))
                return JsonResponse({"error": str(error)}, status=500, safe=False)

        return wrapper

    return decor


class Sql:
    @staticmethod
    def table_init():
        with Sql.connect_db(Utils.get_database_path("local_settings.db")) as connection:
            Sql.execute_query(
                connection,
                """
                CREATE TABLE IF NOT EXISTS params (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT UNIQUE NOT NULL,
                    value TEXT NOT NULL DEFAULT ''
                );
                """,
            )

    @staticmethod
    def save_error_to_db(error_message: str):
        try:
            with Sql.connect_db(Utils.get_database_path("error_log.db")) as connection:
                Sql.execute_query(
                    connection,
                    """
                    INSERT INTO error_log (timestamp, message)
                    VALUES (?, ?);
                    """,
                    (datetime.now(), error_message),
                )
        except Exception as db_error:
            print(f"Database error while saving error log: {db_error}")

    @staticmethod
    def sql_execute(_query: str, _kwargs: dict, _source: str):
        try:
            with Sql.connect_db(Utils.get_database_path(_source)) as connection:
                return Sql.execute_query(connection, _query, _kwargs)
        except Exception as error:
            Sql.save_error_to_db(str(error))
            return None

    @staticmethod
    def connect_db(db_path):
        return sqlite3.connect(db_path)

    @staticmethod
    def execute_query(connection, query, parameters=None):
        with connection:
            cursor = connection.cursor()
            cursor.execute(query, parameters)
            return cursor.fetchall()
