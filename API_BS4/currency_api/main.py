from flask import Flask, render_template
import requests
from datetime import datetime

app = Flask(
    __name__,
    static_url_path="/static",
    static_folder="static",
    template_folder="templates",
)
api_url = "https://api.binance.com/api/v3/klines"
symbol = "BTCUSDT"
interval = "1h"
limit = 5


def format_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp / 1000).strftime("%H:%M:%S %d-%m-%Y")


@app.route("/")
def index():
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(api_url, params=params)

    if response.status_code == 200:
        data = response.json()
        exchange_data = [
            {
                "timestamp": format_timestamp(entry[0]),
                "open": entry[1],
                "high": entry[2],
                "low": entry[3],
                "close": entry[4],
            }
            for entry in data
        ]

        return render_template("index.html", exchange_data=exchange_data)
    else:
        return f"Error: Binance API. Status Code: {response.status_code}"


if __name__ == "__main__":
    app.run(debug=True)
