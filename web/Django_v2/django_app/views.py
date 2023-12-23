"""
views - контроллеры(вью) - т.е. бизнес логика
"""

import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django_app import utils
from django_app.utils import decorator_error_handler
from django_app.models import Product, Review
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.cache import cache
from django.http import Http404


@decorator_error_handler
def home(request):
    result_data = cache.get("home_result_data")

    if result_data is None:
        result_data = utils.get_exchange_data()
        cache.set("home_result_data", result_data, 60 * 60)

    return render(
        request,
        "home.html",
        context={
            "result_data": result_data,
            "date": datetime.date.today(),
        },
    )


def about(request):
    return render(request, "about.html", context={})


def profile(request, username):
    return render(request, "profile.html", context={"username": username})


@decorator_error_handler
def product_list(request):
    data = {
        "database_id": 2,
        "query": "SELECT id, name, DESCRIPTION, price FROM product",
        "many": True,
    }

    products = utils.api_request(data=data, res_type=list)
    return render(request, "product_list.html", {"products": products})


def is_staff(user):
    return user.is_staff


@decorator_error_handler
def product_detail(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return render(request, "error.html", {"error": "Product not found"}, status=404)

    reviews = Review.objects.filter(product=product)

    if (
        request.method == "POST"
        and request.user.is_authenticated
        and request.user.is_staff
    ):
        review_id = request.POST.get("review_id")
        action = request.POST.get("action")

        try:
            review = Review.objects.get(id=review_id, product=product)
        except Review.DoesNotExist:
            raise Http404("Review not found")

        if action == "hide":
            review.is_visible = False
        elif action == "unhide":
            review.is_visible = True

        review.save()
        return redirect("product_detail", product_id=product_id)

    if not request.user.is_staff:
        reviews = reviews.filter(is_visible=True)

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "date": datetime.date.today(),
        },
    )


@decorator_error_handler
def add_review(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=product_id)
        content = request.POST.get("content")

        Review.objects.create(
            product=product, user=request.user, content=content, is_visible=True
        )

    return redirect("product_detail", product_id=product_id)


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("profile", username=username)

    return render(request, "login.html", context={})


@decorator_error_handler
def register(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get("lastname")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, "register.html", {"error": "Passwords do not match"})

        data = {
            "database_id": 1,
            "query": "SELECT username FROM auth_user WHERE username=?",
            "args": (username,),
            "many": False,
        }
        existing_user = utils.api_request(data=data, res_type=list)

        if existing_user:
            return render(
                request, "register.html", {"error": "Username already exists"}
            )
        create_user = {
            "database_id": 1,
            "query": "INSERT INTO auth_user (username, email, password, is_superuser, is_staff, is_active, date_joined, first_name, last_name) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            "args": (
                username,
                email,
                make_password(password),
                "0",
                "0",
                "1",
                datetime.datetime.now().isoformat(),
                firstname,
                lastname,
            ),
            "commit": True,
        }

        utils.api_request(data=create_user, res_type=None)
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