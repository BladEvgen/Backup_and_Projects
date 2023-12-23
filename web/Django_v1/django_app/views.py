"""
views - контроллеры(вью) - т.е. бизнес логика
"""

import datetime
from django.shortcuts import render, redirect
from django_app import utils
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from pathlib import Path
from datetime import date


PRODUCT_DATABASE: str = "database/database.db"
MAIN_DB = Path(__file__).resolve().parent.parent / "db.sqlite3"


def home(request):
    result_data = utils.get_exchange_data()
    return render(
        request,
        "home.html",
        context={
            "result_data": result_data,
            "date": date.today(),
        },
    )


def about(request):
    return render(request, "about.html", context={})


def profile(request, username):
    return render(request, "profile.html", context={"username": username})


def product_list(request):
    db: utils.Database = utils.Database(PRODUCT_DATABASE)

    db.query(
        """
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL unique,
            DESCRIPTION TEXT,
            price REAL NOT NULL DEFAULT 1000
        )
        """,
        commit=True,
    )

    # db.query(
    #     """
    #     INSERT INTO product (name, description, price) VALUES
    #         ('Пылесос', 'Сильный мощный легкий и красивый и все это ваш новый пылесос', 45000.99),
    #         ('Дрон', 'DJI MINI 2, эта игрушку для взрослых принесет много радости в ваш дом', 25999.99),
    #         ('Картина', 'Такая есть только в нашем магазине и у Барак Обамы, больше нигде не найдете похожей', 1000000),
    #         ('Ковер', 'Это не обычный ковер, он висел у самого киевского царя в спальне, можно использовать по назначению или также постелить на пол в прихожей', 0.000001),
    #         ('Микрофон', 'Обычный конденсаторный микрофон ничего удивительного в нем нет', 999.99),
    #         ('Кубик Рубика', 'Легкая и веселая забава детского уровня, каждый взрослый справится с ним', 100.500)
    #     """,
    #     commit=True,
    # )
    products = db.query("SELECT id, name, DESCRIPTION, price FROM product")
    return render(request, "product_list.html", {"products": products})


def product_detail(request, product_id):
    db: utils.Database = utils.Database(PRODUCT_DATABASE)

    product_details = db.query(
        "SELECT * FROM product WHERE id=?", (product_id,), many=False
    )

    if product_details:
        return render(
            request, "product_detail.html", {"product_details": product_details}
        )

    return render(request, "product_detail.html", {"error": "Product not found"})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profile", username=username)

    return render(request, "login.html", context={})


def register(request):
    print(MAIN_DB)
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

        db: utils.Database = utils.Database(MAIN_DB)

        existing_user = db.query(
            "SELECT username FROM auth_user WHERE username=?", (username,), many=False
        )

        if existing_user:
            return render(
                request, "register.html", {"error": "Username already exists"}
            )

        db.query(
            """
            INSERT INTO auth_user (username, email, password, is_superuser, is_staff, is_active, date_joined, first_name, last_name)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
            """,
            (
                username,
                email,
                make_password(password),
                "0",
                "0",
                "1",
                datetime.datetime.now(),
                firstname,
                lastname,
            ),
            commit=True,
        )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile", username=username)

    return render(request, "register.html", context={})


def logout_view(request):
    logout(request)
    return redirect("home")


# First Name: John
# Last Name: Doe
# Email: john.doe@example.com
# Username: johndoe
# Password: securepassword123
