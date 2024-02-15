import os
import datetime
import json
import sys
import asyncio
from PyQt6 import uic
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QWidget, QApplication
import aiosqlite
import aiohttp


class Utils:
    BASE_PATH = os.path.abspath(os.path.join("django_digital_home", "desktop", "src"))
    CONFIG_FILE = os.path.join(BASE_PATH, "config.json")

    @staticmethod
    async def get_database_path(database_filename):
        base_path = os.path.join(Utils.BASE_PATH, "database")
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

        @staticmethod
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
        except Exception as error:
            Utils.save_error_to_db(str(error))

    @staticmethod
    async def create_error_log_table():
        try:
            connection = await aiosqlite.connect(
                await Utils.get_database_path("error_log.db")
            )
            cursor = await connection.cursor()
            await cursor.execute(Utils.Query.create_table_error_log())
            await connection.commit()
        except Exception as db_error:
            print(f"Database error while creating error log table: {db_error}")
        finally:
            await connection.close()

    @staticmethod
    async def save_error_to_db(error_message: str):
        try:
            connection = await aiosqlite.connect(
                await Utils.get_database_path("error_log.db")
            )
            await connection.execute(
                """
                INSERT INTO error_log (timestamp, message)
                VALUES (?, ?)
                """,
                (datetime.datetime.now(), error_message),
            )
            print(f"\n\n\n{error_message}\n\n")
            await connection.commit()
        except Exception as db_error:
            print(f"Database error while saving error: {db_error}")
        finally:
            await connection.close()

    @staticmethod
    async def sql_execute(query: str, kwargs: dict, source: str):
        try:
            async with aiosqlite.connect(
                await Utils.get_database_path(source)
            ) as connection:
                await connection.execute(query, kwargs)
                await connection.commit()
                if "params" in query:
                    async with connection.execute(
                        Utils.Query.get_all_params()
                    ) as cursor:
                        data = await cursor.fetchall()
                else:
                    data = None
            return data
        except Exception as error:
            await Utils.save_error_to_db(str(error))
            return None

    @staticmethod
    async def database_init():
        Utils.load_config()
        await Utils.create_error_log_table()
        await Utils.sql_execute(
            query=Utils.Query.create_table_params(),
            kwargs={},
            source="local_settings.db",
        )
        await Utils.sql_execute(
            query=Utils.Query.create_table_error_log(),
            kwargs={},
            source="error_log.db",
        )

    @staticmethod
    async def sync_settings_to_web():
        rows = await Utils.sql_execute(
            query=Utils.Query.get_all_params(), kwargs={}, source="local_settings.db"
        )
        if rows is not None:
            params = dict((str(x[0]), str(x[1])) for x in rows)
            try:
                async with aiohttp.ClientSession() as session:
                    await Utils._post_settings(session, params)
            except aiohttp.ClientError as client_error:
                await Utils.save_error_to_db(f"HTTP error occurred: {client_error}")
            except Exception as error:
                await Utils.save_error_to_db(f"An error occurred: {error}")

    @staticmethod
    async def sync_settings_from_web():
        try:
            async with aiohttp.ClientSession() as session:
                data = await Utils._get_settings(session)
                for k, v in data.items():
                    await Utils.sql_execute(
                        query=Utils.Query.get_insert_or_replace_params(),
                        kwargs={"key": str(k), "value": str(v)},
                        source="local_settings.db",
                    )
        except aiohttp.ClientError as client_error:
            await Utils.save_error_to_db(f"HTTP error occurred: {client_error}")
        except Exception as error:
            await Utils.save_error_to_db(f"An error occurred: {error}")

    @staticmethod
    async def _post_settings(session, params):
        async with session.post(
            f"http://{Utils.HOST}:{Utils.PORT}/api/settings/set/",
            headers={"Authorization": "Token=auth1234"},
            data=json.dumps({"id": "970801", "params": params}),
        ) as response:
            response.raise_for_status()
            if response.status not in (200, 201):
                raise Exception(f"WEB ERROR {response.status}")

    @staticmethod
    async def _get_settings(session):
        async with session.get(
            f"http://{Utils.HOST}:{Utils.PORT}/api/settings/get/",
            headers={"Authorization": "Token=auth123"},
        ) as response:
            response.raise_for_status()
            if response.status not in (200, 201):
                raise Exception(f"WEB ERROR {response.status}")
            data = await response.json()
            return data.get("data", {})

    @staticmethod
    async def loop(target: callable, args: tuple, delay: float, prefix: str):
        while True:
            try:
                await target(*args, prefix)
            except Exception as error:
                await Utils.save_error_to_db(
                    f"{datetime.datetime.now()} {prefix}: {error}"
                )
            await asyncio.sleep(delay)


class Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi(os.path.join(Utils.BASE_PATH, "main.ui"), self)
        self.params = {}

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

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(100)

    def on_timer(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.update_ui_from_local_settings())

    async def push_button_temp_plan(self, delta, key):
        rows = await Utils.sql_execute(
            query=Utils.Query.get_all_params(), kwargs={}, source="local_settings.db"
        )
        if rows is not None:
            params = dict((str(x[0]), str(x[1])) for x in rows)
            params[key] = str(int(params.get(key, -7)) + delta)
            await Utils.sql_execute(
                query=Utils.Query.get_insert_or_replace_params(),
                kwargs={"key": str(key), "value": str(params[key])},
                source="local_settings.db",
            )
            await Utils.sync_settings_to_web()

    def push_button_temp_plan_plus(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.push_button_temp_plan(1, "temp_plan_high"))

    def push_button_temp_plan_minus(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.push_button_temp_plan(-1, "temp_plan_high"))

    def push_button_temp_plan_plus_freezer(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.push_button_temp_plan(1, "temp_plan_down"))

    def push_button_temp_plan_minus_freezer(self):
        loop = asyncio.get_event_loop()
        loop.create_task(self.push_button_temp_plan(-1, "temp_plan_down"))

    async def update_ui_from_local_settings(self):
        rows = await Utils.sql_execute(
            query=Utils.Query.get_all_params(), kwargs={}, source="local_settings.db"
        )
        if rows is not None:
            params = dict((str(x[0]), str(x[1])) for x in rows)
            self.params["temp_plan_high"] = int(params.get("temp_plan_high", -7))
            self.params["temp_plan_down"] = int(params.get("temp_plan_down", -20))
            QApplication.processEvents()
            self.ui.label_temp_plan_high.setText(str(self.params["temp_plan_high"]))
            self.ui.label_temp_plan_down.setText(str(self.params["temp_plan_down"]))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Utils.database_init())
    app = QApplication(sys.argv)
    ui = Ui()
    sys.exit(app.exec())
