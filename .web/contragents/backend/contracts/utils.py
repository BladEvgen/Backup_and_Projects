import json
import os
import re
import threading
from datetime import datetime
from functools import wraps

import requests
from django.conf import settings
from django.http import HttpRequest

log_lock = threading.Lock()


def gin_log_decorator(func):
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        try:
            response = func(request, *args, **kwargs)
        except Exception as error:
            response = None
            error_message = str(error)
        else:
            error_message = (
                response.data.get("message", "Unknown error")
                if hasattr(response, "data")
                else "Unknown error"
            )

        log_data = {
            "ip": request.META.get("REMOTE_ADDR"),
            "timestamp": int(datetime.now().timestamp()),
            "status_code": response.status_code if response else 500,
            "method": request.method,
            "path": request.path,
            "user_agent": request.META.get("HTTP_USER_AGENT"),
            "message": (
                "OK"
                if request.method == "GET" and response.status_code == 200
                else error_message
            ),
            "username": (
                request.user.username if request.user.is_authenticated else "anonymous"
            ),
        }

        def log_to_remote():
            try:
                requests.post("http://localhost:8001/api/logs", json=log_data)
            except Exception as e:
                print(f"Error logging to remote: {e}")

        threading.Thread(target=log_to_remote).start()

        today = datetime.now().strftime("%H-%d-%m-%Y")
        log_path = os.path.join(settings.BASE_DIR, f"logs/log_{today}.log")
        log_list = []

        try:
            with open(log_path, "r", encoding="utf-8") as f:
                log_list = json.load(f)
        except FileNotFoundError:
            pass

        log_list.append(log_data)

        with log_lock:
            with open(log_path, "w", encoding="utf-8") as f:
                json.dump(log_list, f, indent=4, ensure_ascii=False)

        return response

    return wrapper


def password_check(password: str) -> bool:
    return bool(
        re.match(
            r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$", password
        )
    )


def transliterate(name):
    slovar = {
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "yo",
        "ж": "zh",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "h",
        "ц": "ts",
        "ч": "ch",
        "ш": "sh",
        "щ": "sch",
        "ъ": "",
        "ы": "y",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
        " ": " ",
        "-": "-",
        ".": ".",
        ",": ",",
        "!": "!",
        "?": "?",
        ":": ":",
    }

    name = name.lower()

    translit = ""
    for letter in name:
        if letter in slovar:
            translit += slovar[letter]
        else:
            translit += letter

    return translit
