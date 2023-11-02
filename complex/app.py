from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
import os

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="templates",
)


local_path = os.path.join(os.path.dirname(__file__), "db")
os.makedirs(local_path, exist_ok=True)

class Database:
    @staticmethod
    def query(query_str: str, args=(), many=True):
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
    @staticmethod
    def create_db():
        Database.query(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                description TEXT
            )
            """
        )

    @staticmethod
    def drop_db():
        Database.query("DROP TABLE IF EXISTS tasks")

    @staticmethod
    def insert_task(task: str, description: str = None):
        query_str = """
        INSERT INTO tasks (task, description)
        VALUES (?, ?)
        """
        task_data = (task, description)
        Database.query(query_str, task_data)


# DatabaseTools.drop_db()
DatabaseTools.create_db()



@app.route("/")
def main_page():
    tasks = Database.query("SELECT task, description FROM tasks")
    return render_template("index.html", tasks=tasks)

@app.route("/delete_task", methods=["POST"])
def delete_task():
    task_to_delete = request.form.get("task")
    if task_to_delete:
        query_str = "DELETE FROM tasks WHERE task = ?"
        Database.query(query_str, (task_to_delete,))
    return redirect(url_for("main_page"))

@app.route("/get_tasks_json", methods=["GET"])
def get_tasks_json():
    tasks = Database.query("SELECT task, description FROM tasks")
    tasks_dict = [{"task": task, "description": description} for task, description in tasks]
    return jsonify(tasks_dict)


@app.route("/add_task", methods=["POST"])
def add_task():
    task = request.form["task"]
    description = request.form.get("description")
    DatabaseTools.insert_task(task, description)
    return redirect(url_for("main_page"))

if __name__ == "__main__":
    app.run()
