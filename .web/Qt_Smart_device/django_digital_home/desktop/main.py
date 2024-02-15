import os
import datetime
import json
import sys
import threading
import time
from PyQt6 import uic
from PyQt6.QtWidgets import QWidget, QApplication
import sqlite3
import requests


class Utils:
    CONFIG_FILE = os.path.abspath(
        os.path.join("django_digital_home", "desktop", "src", "config.json")
    )

    @staticmethod
    def get_database_path(database_filename):
        base_path = os.path.abspath(
            os.path.join("django_digital_home", "desktop", "src", "database")
        )
        return os.path.join(base_path, database_filename)

    class Query:
        @staticmethod
        def create_table_error_log() -> str:
            return """
                CREATE TABLE IF NOT EXISTS error_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    message TEXT NOT NULL
                );
                """

        def create_table_params() -> str:
            return """
                CREATE TABLE IF NOT EXISTS params (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL
                );
                """

        @staticmethod
        def get_all_params() -> str:
            return """
                SELECT key, value 
                FROM params
                ;"""

        @staticmethod
        def get_insert_or_replace_params() -> str:
            return """
                INSERT OR REPLACE 
                INTO params
                    (key, value)
                VALUES
                    (:key, :value)
                ;"""

    @staticmethod
    def load_config():
        try:
            with open(Utils.CONFIG_FILE, "r") as config_file:
                config = json.load(config_file)
                Utils.HOST = config.get("host", "")
                Utils.PORT = config.get("port", "")
                Utils.SERIAL_ID = config.get("serial_id", "")
        except Exception as error:
            Utils.save_error_to_db(str(error))

    @staticmethod
    def create_error_log_table():
        try:
            with sqlite3.connect(Utils.get_database_path("error_log.db")) as connection:
                connection.execute(Utils.Query.create_table_error_log())
        except Exception as db_error:
            print(f"Database error while creating error log table: {db_error}")

    @staticmethod
    def save_error_to_db(error_message: str):
        try:
            with sqlite3.connect(Utils.get_database_path("error_log.db")) as connection:
                connection.execute(
                    """
                    INSERT INTO error_log (timestamp, message)
                    VALUES (?, ?)
                    """,
                    (datetime.datetime.now(), error_message),
                )
        except Exception as db_error:
            print(f"Database error while saving error: {db_error}")

    @staticmethod
    def sql_execute(_query: str, _kwargs: dict, _source: str):
        try:
            with sqlite3.connect(Utils.get_database_path(_source)) as _connection:
                _connection.execute(_query, _kwargs)
                if "params" in _query:
                    _data = _connection.execute(Utils.Query.get_all_params()).fetchall()
                else:
                    _data = None
            return _data
        except Exception as error:
            Utils.save_error_to_db(str(error))
            return None

    @staticmethod
    def database_init():
        Utils.load_config()
        Utils.create_error_log_table()
        Utils.sql_execute(
            _query=Utils.Query.create_table_params(),
            _kwargs={},
            _source="local_settings.db",
        )
        Utils.sql_execute(
            _query=Utils.Query.create_table_error_log(),
            _kwargs={},
            _source="error_log.db",
        )

    @staticmethod
    def sync_settings_to_web():
        _rows = Utils.sql_execute(
            _query=Utils.Query.get_all_params(),
            _kwargs={},
            _source="local_settings.db",
        )
        if _rows is not None:
            _params = dict((str(x[0]), str(x[1])) for x in _rows)
            try:
                _response = requests.post(
                    url=f"http://{Utils.HOST}:{Utils.PORT}/api/settings/set/",
                    headers={
                        "Authorization": "Token=auth1234",
                        "serial_id": Utils.SERIAL_ID,
                    },
                    data=json.dumps({"params": _params}),
                )
                _response.raise_for_status()
                if _response.status_code not in (200, 201):
                    raise Exception(f"WEB ERROR {_response.status_code}")
            except requests.exceptions.HTTPError as http_error:
                Utils.save_error_to_db(f"HTTP error occurred: {http_error}")
            except Exception as error:
                Utils.save_error_to_db(f"An error occurred: {error}")

    @staticmethod
    def sync_settings_from_web():
        try:
            _response = requests.get(
                f"http://{Utils.HOST}:{Utils.PORT}/api/settings/get/",
                headers={"Authorization": "Token=auth123"},
            )
            _response.raise_for_status()
            if _response.status_code not in (200, 201):
                raise Exception(f"WEB ERROR {_response.status_code}")
            _data = _response.json().get("data", {})
            with sqlite3.connect(
                Utils.get_database_path("local_settings.db")
            ) as connection:
                for k, v in _data.items():
                    if k == "temp_plan_down":
                        connection.execute(
                            Utils.Query.get_insert_or_replace_params(),
                            {"key": str(k), "value": str(v)},
                        )
        except requests.exceptions.HTTPError as http_error:
            Utils.save_error_to_db(f"HTTP error occurred: {http_error}")
        except Exception as error:
            Utils.save_error_to_db(f"An error occurred: {error}")

    @staticmethod
    def loop(target: callable, args: tuple, delay: float | int, prefix: str):
        while threading.main_thread().is_alive():
            try:
                threading.Thread(target=target, args=args, daemon=True).start()
            except Exception as error:
                Utils.save_error_to_db(f"{datetime.datetime.now()} {prefix}: {error}")
            time.sleep(delay)


class Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(
            os.path.join("django_digital_home", "desktop", "src", "main.ui"),
            self,
        )
        self.__params = {}

        self.ui.pushButton_temp_plan_plus.clicked.connect(
            self.push_button_temp_plan_plus
        )
        self.ui.pushButton_temp_plan_minus.clicked.connect(
            self.push_button_temp_plan_minus
        )
        self.ui.pushButton_temp_plan_plus_freezer.clicked.connect(
            self.push_button_temp_plan_plus_freezer
        )
        self.ui.pushButton_temp_plan_minus_freezer.clicked.connect(
            self.push_button_temp_plan_minus_freezer
        )

        self.show()
        threading.Thread(target=self.loop, daemon=True).start()

    def push_button_temp_plan(self, delta, key):
        _rows = Utils.sql_execute(
            _query=Utils.Query.get_all_params(),
            _kwargs={},
            _source="local_settings.db",
        )
        if _rows is not None:
            _params = dict((str(x[0]), str(x[1])) for x in _rows)
            _params[key] = str(int(_params.get(key, -7)) + delta)
            Utils.sql_execute(
                _query=Utils.Query.get_insert_or_replace_params(),
                _kwargs={"key": str(key), "value": str(_params[key])},
                _source="local_settings.db",
            )
            threading.Thread(target=Utils.sync_settings_to_web, daemon=True).start()

    def push_button_temp_plan_plus(self):
        self.push_button_temp_plan(1, "temp_plan_high")

    def push_button_temp_plan_minus(self):
        self.push_button_temp_plan(-1, "temp_plan_high")

    def push_button_temp_plan_plus_freezer(self):
        self.push_button_temp_plan(1, "temp_plan_down")

    def push_button_temp_plan_minus_freezer(self):
        self.push_button_temp_plan(-1, "temp_plan_down")

    def update_ui_from_local_settings(self):
        _rows = Utils.sql_execute(
            _query=Utils.Query.get_all_params(),
            _kwargs={},
            _source="local_settings.db",
        )
        if _rows is not None:
            _params = dict((str(x[0]), str(x[1])) for x in _rows)
            self.__params["temp_plan_high"] = int(_params.get("temp_plan_high", -7))
            self.__params["temp_plan_down"] = int(_params.get("temp_plan_down", -20))
            self.ui.label_temp_plan_high.setText(str(self.__params["temp_plan_high"]))
            self.ui.label_temp_plan_down.setText(str(self.__params["temp_plan_down"]))

    def loop(self):
        while threading.main_thread().is_alive():
            Utils.loop(
                self.update_ui_from_local_settings,
                (),
                0.1,
                "update_ui_from_local_settings",
            )
            Utils.loop(
                Utils.sync_settings_from_web, (), 3.0, "Utils.sync_settings_from_web"
            )


if __name__ == "__main__":
    Utils.database_init()
    app = QApplication(sys.argv)
    ui = Ui()
    sys.exit(app.exec())
