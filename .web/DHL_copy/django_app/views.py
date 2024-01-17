import pandas as pd
from pathlib import Path
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django_app.utils import decorator_error_handler, generate_random_prices, Database
from django.core.cache import cache
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import Price
from .forms import UploadFileForm

MAIN_DB = Path(__file__).resolve().parent.parent / "db.sqlite3"
DB_PATH = Path(__file__).resolve().parent.parent / "database" / "database.db"


def about(request):
    return render(request, "about.html", context={})


def success_page(request):
    return render(request, "success_page.html")


@decorator_error_handler
def home(request):
    return render(request, "home.html", context={})


@decorator_error_handler
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("price_list")

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

        existing_user = User.objects.filter(username=username).exists()
        if existing_user:
            return render(
                request, "register.html", {"error": "Username already exists"}
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=firstname,
            last_name=lastname,
        )

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("profile", username=username)
        else:
            return render(
                request,
                "register.html",
                {"error": "Failed to log in. Please try again."},
            )

    return render(request, "register.html", context={})


def logout_view(request):
    logout(request)
    return redirect("home")


@decorator_error_handler
def profile(request, username):
    return render(request, "profile.html", context={"username": username})


@decorator_error_handler
def price_list(request):
    cache_key = f"price_list_{request.GET.get('page', 1)}"

    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result

    selected_page = request.GET.get("page", 1)
    prices = Price.objects.all()
    p = Paginator(object_list=prices, per_page=40)

    try:
        current_page = p.page(number=selected_page)
    except Exception:
        current_page = p.page(p.num_pages)

    page_range_start = max(1, current_page.number - 2)
    page_range_end = min(p.num_pages, current_page.number + 1)
    page_range = range(page_range_start, page_range_end + 1)

    result = render(
        request,
        "price_list.html",
        context={"page_obj": current_page, "page_range": page_range},
    )

    cache.set(cache_key, result, 5)

    return result


@decorator_error_handler
def price_list_sql(request):
    selected_page = int(request.GET.get("page", 1))
    items_per_page = 20

    cache_key = f"price_list_sql_page_{selected_page}"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    sql_query = """
        SELECT id, name, description, price
        FROM django_app_price
    """

    db = Database(MAIN_DB)
    prices = db.query(sql_query, many=True)

    p = Paginator(prices, items_per_page)

    try:
        current_page = p.page(selected_page)
    except Exception:
        current_page = p.page(p.num_pages)

    page_range_start = max(1, current_page.number - 2)
    page_range_end = min(p.num_pages, current_page.number + 1)
    page_range = range(page_range_start, page_range_end + 1)

    cache.set(
        cache_key,
        render(
            request,
            "price_list_sql.html",
            context={"page_obj": current_page, "page_range": page_range},
        ),
        10,
    )

    return render(
        request,
        "price_list_sql.html",
        context={"page_obj": current_page, "page_range": page_range},
    )


@decorator_error_handler
def load_data(request):
    db = Database(DB_PATH)
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES["file"]
            df = pd.read_excel(uploaded_file)
            for index, row in df.iterrows():
                title = row["title"]
                description = row["description"]
                price = row["price"]
                is_active = True
                query_str = """
                    INSERT INTO price_data (title, description, price, is_active)
                    VALUES (?, ?, ?, ?);
                """
                db.query(query_str, (title, description, price, is_active), commit=True)
            return redirect("success_page")

    else:
        form = UploadFileForm()

    return render(request, "load_data.html", {"form": form})


@decorator_error_handler
def price_list_xlsx(request):
    db = Database(DB_PATH)
    cache_key = f"price_list_{request.GET.get('page', 1)}"

    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result

    selected_page = request.GET.get("page", 1)

    query_str = "SELECT id, title, description, price, is_active FROM price_data"
    prices = db.query(query_str, many=True)

    p = Paginator(object_list=prices, per_page=4) 

    try:
        current_page = p.page(number=selected_page)
    except Exception:
        current_page = p.page(p.num_pages)

    page_range_start = max(1, current_page.number - 2)
    page_range_end = min(p.num_pages, current_page.number + 1)
    page_range = range(page_range_start, page_range_end + 1)

    result = render(
        request,
        "price_list_xlsx.html",
        context={"page_obj": current_page, "page_range": page_range},
    )

    cache.set(cache_key, result, 5)

    return result
