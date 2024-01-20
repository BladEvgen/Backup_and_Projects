import qrcode
from io import BytesIO
from django.shortcuts import render, get_object_or_404, redirect
from .models import Wine, WineReview, Winery, WineCategory
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.utils import timezone
from django.utils.translation import activate


def create_wine(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        production_date = request.POST.get("production_date")
        expiration_date = request.POST.get("expiration_date")
        winery_id = request.POST.get("winery")
        category_id = request.POST.get("category")
        picture = request.FILES.get("picture")

        try:
            winery = Winery.objects.get(id=winery_id)
            category = WineCategory.objects.get(id=category_id)
        except Winery.DoesNotExist:
            messages.error(request, "Selected Winery does not exist.")
            return redirect("create_wine")
        except WineCategory.DoesNotExist:
            messages.error(request, "Selected Category does not exist.")
            return redirect("create_wine")

        wine = Wine.objects.create(
            name=name,
            description=description,
            production_date=production_date,
            expiration_date=expiration_date,
            winery=winery,
            category=category,
            picture=picture,
        )

        wine_url = f"http://172.20.10.9:8000{wine.get_absolute_url()}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(wine_url)
        qr.make(fit=True)

        qr_code_img = qr.make_image(fill_color="black", back_color="white")

        buffer = BytesIO()
        qr_code_img.save(buffer, format="PNG")

        qr_code_path = default_storage.save(
            f"qr_codes/{wine.id}.png", ContentFile(buffer.getvalue())
        )

        wine.qr_code.name = qr_code_path
        wine.save()

        return redirect(wine.get_absolute_url())
    else:
        wineries = Winery.objects.all()
        categories = WineCategory.objects.all()
        return render(
            request,
            "create_product.html",
            {"wineries": wineries, "categories": categories},
        )


def wine_detail(request, wine_id):
    wine = get_object_or_404(Wine, id=wine_id)
    reviews = WineReview.objects.filter(wine=wine)
    selected_language = request.COOKIES.get("selected_language", "ENG")
    activate(selected_language)

    return render(
        request,
        "product_detail.html",
        {"wine": wine, "reviews": reviews, "selected_language": selected_language},
    )


def home(request):
    selected_language = request.COOKIES.get("selected_language", "ENG")
    activate(selected_language)
    wines = Wine.objects.filter(expiration_date__gt=timezone.now().date())
    return render(request, "home.html", context={"wines": wines, "selected_language": selected_language})


def logout_view(request):
    logout(request)
    return redirect("home")


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Invalid username or password. Please try again.")

    return render(request, "login.html")


def profile(request, username):
    selected_language = request.COOKIES.get("selected_language", "ENG")
    activate(selected_language)
    return render(
        request,
        "profile.html",
        context={"username": username, "selected_language": selected_language},
    )


def register(request):
    if request.method == "POST":
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
            password=password,
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
