import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, session, redirect, url_for


app = Flask(__name__)
app.secret_key = "secret_key_777"

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)


API_KEY_WEATHER = os.getenv("API_KEY_WEATHER")
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
GEO_BASE_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_URL = f"{WEATHER_BASE_URL}?appid={API_KEY_WEATHER}&lang=ru"
GEO_URL = f"{GEO_BASE_URL}?limit=1&appid={API_KEY_WEATHER}"


def get_weather(city):
    url = f"{WEATHER_URL}&q={city}"
    res = requests.get(url)
    res.raise_for_status()
    data = res.json()

    if "main" not in data:
        return {"error": "Weather data not found"}

    convert_kelvin_to_celsius = lambda k: round(k - 273.15, 1)

    return {
        "temp": convert_kelvin_to_celsius(data["main"]["temp"]),
        "feels_like": convert_kelvin_to_celsius(data["main"]["feels_like"]),
        "temp_min": convert_kelvin_to_celsius(data["main"]["temp_min"]),
        "temp_max": convert_kelvin_to_celsius(data["main"]["temp_max"]),
        "pressure": data["main"]["pressure"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "wind_direction": data["wind"]["deg"],
        "desc": data["weather"][0]["description"].capitalize(),
        "icon_name": data["weather"][0]["icon"],
    }


def get_country_code(city):
    try:
        url = f"{GEO_URL}&q={city}"
        response = requests.get(url)
        content = response.json()

        if content:
            return content[0]["country"]
    except requests.exceptions.RequestException:
        return None


def get_city_from_ip():
    try:
        response = requests.get("https://ipinfo.io/")
        data = response.json()
        return data.get("city")
    except requests.exceptions.RequestException:
        return None


@app.route("/clear_requests")
def clear_requests():
    session.clear()
    return "Requests cleared!"


@app.route("/", methods=["GET", "POST"])
def home():
    city = request.args.get("city") or get_city_from_ip()
    weather_data = get_weather(city)
    is_country_code = get_country_code(city)
    if request.method == "POST" and request.form.get("clear"):
        session.clear()
        return redirect(url_for("home"))
    return render_template(
        "home.html",
        city=city,
        weather_data=weather_data,
        is_country_code=is_country_code,
    )


if __name__ == "__main__":
    app.run(debug=True, port=8000)
