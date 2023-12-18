from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
    "authority": "store.playstation.com",
    "sec-ch-ua-platform": '"Windows"',
}


@app.route("/")
def index():
    url = "https://www.mig.kz/"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")

    exchange_data = soup.find("ul", class_="clearfix").find_all("li")

    currencies = ["USD", "EUR", "RUB", "KGS", "GBP", "CNY", "GOLD"]

    result_data = [
        (currencies[i], exchange_data[i].text.strip()) for i in range(len(currencies))
    ]

    return render_template("index.html", result_data=result_data)


if __name__ == "__main__":
    app.run(debug=True, port=8000)
