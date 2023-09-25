import os
import psycopg2
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


def config_db():
    db_settings = {
        "host": os.getenv("DB_HOST"),
        "port": os.getenv("DB_PORT"),
        "dbname": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
    }
    return db_settings


def create_table():
    table_name = "users"
    query_str = f"""
    CREATE TABLE {table_name} (
        id SERIAL PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL
    );
    """
    query(query_str, many=False)
    print(f"Table '{table_name}' created successfully.")


def query(query_str: str, args=(), many=True) -> list | None:
    try:
        db_settings = config_db()
        with psycopg2.connect(**db_settings) as connection:
            with connection.cursor() as cursor:
                cursor.execute(query_str, args)
                if many:
                    return cursor.fetchall()
                return cursor.fetchone()
    except Exception as e:
        print(f"Error executing query: {e}")
        return None


def insert_data(username, email):
    query_str = "INSERT INTO users (username, email) VALUES (%s, %s) RETURNING id;"
    args = (username, email)
    return query(query_str, args, many=False)


def select_data(user_id):
    query_str = "SELECT * FROM users WHERE id = %s;"
    args = (user_id,)
    return query(query_str, args, many=False)


def main():
    user_id = insert_data("doe_john", "johndoe@example.com")
    if user_id:
        print("User inserted")

    user = select_data(user_id)
    if user:
        print(f"Selected user: {user}")


if __name__ == "__main__":
    main()
