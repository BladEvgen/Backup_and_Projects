from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import hashlib

app = Flask(__name__)
app.config["SECRET_KEY"] = "something_secret_666"
DB_NAME = "users.db"


def create_tables():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                date_of_creation TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price REAL NOT NULL,
                description TEXT NOT NULL,
                featured INTEGER DEFAULT 0
            );
        """
        )


def insert_product(product):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO products (name, price, description, featured) 
            VALUES (?, ?, ?, ?)
            ON CONFLICT(name) DO NOTHING;
            """,
            (
                product["name"],
                product["price"],
                product["description"],
                product.get("featured", 0),
            ),
        )
        conn.commit()


def fetch_featured_products():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE featured = 1")
        return cursor.fetchall()


def fetch_all_products():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        return cursor.fetchall()


def fetch_user(username):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user_data = cursor.fetchone()

    if user_data:
        user_dict = {
            "id": user_data[0],
            "username": user_data[1],
            "password": user_data[2],
            "date_of_creation": user_data[3],
        }
        return user_dict
    else:
        return None


def update_password(username, new_password):
    hashed_password = hashlib.sha256(new_password.encode()).hexdigest()
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET password=? WHERE username=?", (hashed_password, username)
        )
        conn.commit()


@app.route("/")
def home():
    featured_products = fetch_featured_products()
    return render_template("home.html", featured_products=featured_products)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/profile/<username>")
def profile(username):
    user = fetch_user(username)
    return render_template("profile.html", user=user)


@app.route("/change_password/<username>", methods=["GET", "POST"])
def change_password(username):
    if request.method == "POST":
        current_password = request.form["current_password"]
        new_password = request.form["new_password"]

        user = fetch_user(username)
        if (
            user
            and user["password"]
            == hashlib.sha256(current_password.encode()).hexdigest()
        ):
            update_password(username, new_password)
            flash("Password updated successfully!", "success")
            return redirect(url_for("profile", username=username))
        else:
            flash("Current password is incorrect", "danger")

    return render_template("change_password.html", username=username)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, password, date_of_creation) VALUES (?, ?, datetime("now"))',
                (username, hashed_password),
            )
            conn.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        with sqlite3.connect("users.db") as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM users WHERE username=? AND password=?",
                (username, hashed_password),
            )
            user = cursor.fetchone()

        if user:
            session["username"] = username
            return redirect(url_for("product_list"))

    return render_template("login.html")


@app.route("/product_list")
def product_list():
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        products = cursor.fetchall()

    return render_template("product_list.html", products=products)


@app.route("/product/<int:product_id>")
def product_details(product_id):
    with sqlite3.connect("users.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
        product = cursor.fetchone()

    if product:
        return render_template("product_details.html", product=product)
    else:
        return "Product not found"


def create_insert():
    try:
        create_tables()
        products_data = [
            {
                "name": "Product 1",
                "price": 19.99,
                "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc at velit quis purus egestas suscipit id vitae enim. Vivamus interdum ex quis orci lobortis ultrices. Etiam volutpat, elit sed dapibus mollis, quam sapien porta sapien, in scelerisque neque mi sit amet mi. In at elit ornare, ornare lorem et, consequat magna. ",
            },
            {
                "name": "Product 2",
                "price": 29.99,
                "description": "Praesent non ante et orci lacinia cursus. Ut aliquet non erat vitae faucibus. Maecenas id magna ante. Aenean suscipit arcu quis condimentum dapibus. Suspendisse porttitor dui quis tortor convallis congue.",
                "featured": 1,
            },
            {
                "name": "Product 3",
                "price": 39.99,
                "description": "Fusce non massa libero. Sed efficitur malesuada eros, vitae pharetra quam scelerisque eget. Integer id est a risus euismod viverra. In hac habitasse platea dictumst. Curabitur pretium orci nec vehicula bibendum. Nulla scelerisque efficitur dolor, ullamcorper volutpat quam pulvinar pellentesque. Aliquam elementum, tortor vel gravida consectetur, risus felis porttitor augue, nec fringilla dui velit vel erat. Morbi vitae bibendum enim. Pellentesque malesuada, erat vitae elementum venenatis, turpis tortor fermentum ante, malesuada volutpat libero neque tempus lorem. Aenean nec luctus metus. Curabitur ex lacus, gravida at libero luctus, convallis bibendum lorem. Fusce rutrum ante ut eros varius finibus. Aliquam eget enim nibh. Duis eleifend at ante vel mollis.",
            },
            {
                "name": "Product 4",
                "price": 49.99,
                "description": "Interdum et malesuada fames ac ante ipsum primis in faucibus. Cras posuere mattis libero at malesuada. Quisque ullamcorper, elit eget convallis varius, diam nibh accumsan massa, ut pulvinar eros mi sit amet metus. Cras viverra, mauris vel congue congue, mauris ipsum accumsan mi, at sodales magna augue a nisl. Ut lobortis massa et velit ultrices dictum. Sed porta dictum velit eget vulputate. Curabitur enim massa, tincidunt a tempus sit amet, ultricies ac lorem.",
                "featured": 1,
            },
            {
                "name": "Product 5",
                "price": 59.99,
                "description": "Ut pulvinar sapien vel dolor feugiat, vitae imperdiet erat dignissim. Donec tempor, dolor vitae pharetra vestibulum, nunc elit fringilla nunc, ac faucibus nunc ex vitae risus. Etiam consectetur quis velit ac fermentum. Ut ut tristique ex. Integer pulvinar tortor nec orci ullamcorper sodales. Sed eget dignissim risus, malesuada mattis enim. Cras lacinia aliquet lectus, in pellentesque orci cursus tincidunt. Maecenas ac ex suscipit, lacinia arcu ut, finibus eros. Fusce quis blandit tortor. Donec at ligula vitae nulla fringilla suscipit.",
                "featured": 1,
            },
            {
                "name": "Product 6",
                "price": 666,
                "description": "TEST PRODUCT",
                "featured": 1,
            },
        ]
        for product in products_data:
            insert_product(product)
    except Exception as e:
        print(f"Error during database initialization: {e}")


create_insert()

if __name__ == "__main__":
    app.run(debug=True)
