import json
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django_app import utils
from django.shortcuts import redirect


def get_params_dict(rows):
    return (
        {x[0]: x[1] for x in rows}
        if rows and isinstance(rows[0], (tuple, dict))
        else {}
    )


def get_params_rows(source_folder="database"):
    try:
        rows = utils.Sql.sql_execute(
            _query="SELECT key, value FROM params;",
            _kwargs={},
            _source=utils.Utils.get_database_path(
                "local_settings.db", source_folder=source_folder
            ),
        )
        return rows
    except Exception as error:
        log_error(f"Error while getting params rows: {error}")
        print(f"Error while getting params rows: {error}")
        return []


def log_error(error_message):
    try:
        utils.Sql.sql_execute(
            _query="INSERT INTO error_log (timestamp, message) VALUES (?, ?);",
            _kwargs=(utils.Utils.get_current_timestamp(), error_message),
            _source=utils.Utils.get_database_path("error_log.db"),
        )
    except Exception as db_error:
        print(f"Database error while saving error log: {db_error}")


def render_error(request, error):
    log_error(str(error))
    print(f"Error occurred: {error}")
    return render(request, "error.html", context={"error_message": str(error)})


def render_home(request, params):
    return render(request, "index.html", context={"params": params})


def home(request):
    try:
        _rows = get_params_rows()
        _params = get_params_dict(_rows)
        return render(request, "index.html", context={"params": _params})
    except Exception as error:
        log_error(str(error))
        print(f"Error occurred: {error}")
        return render(request, "error.html", context={"error_message": str(error)})


def index(request):
    return JsonResponse(data={"message": "OK"})


@api_view(["GET"])
@utils.DRF.decor_error
def settings_get(request):
    try:
        rows = get_params_rows()
        params_dict = get_params_dict(rows)
        data = {
            "temp_plan_high": params_dict.get("temp_plan_high", ""),
            "temp_plan_down": params_dict.get("temp_plan_down", ""),
        }
        return JsonResponse(data)
    except Exception as error:
        log_error(str(error))
        return JsonResponse({"error": str(error)})


@api_view(["POST"])
@utils.DRF.decor_error
@csrf_exempt
def settings_set(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        for k, v in data.get("params", {}).items():
            utils.Sql.sql_execute(
                _query="INSERT OR REPLACE INTO params (key, value) VALUES (:key, :value);",
                _kwargs={"key": str(k), "value": str(v)},
                _source=utils.Utils.get_database_path("local_settings.db"),
            )
        return JsonResponse({"data": "OK"})
    except Exception as error:
        log_error(str(error))
        return JsonResponse({"error": str(error)})


@api_view(["GET"])
@utils.DRF.decor_error
def settings_change(request):
    try:
        name = request.GET.get("name")
        action = request.GET.get("action")

        rows = get_params_rows()
        params_dict = get_params_dict(rows)
        value = int(params_dict.get(name, 0))

        if action == "plus":
            value += 1
        elif action == "minus":
            value -= 1
        else:
            return JsonResponse({"error": "Unknown action!"})

        utils.Sql.sql_execute(
            _query="INSERT OR REPLACE INTO params (key, value) VALUES (:key, :value);",
            _kwargs={"key": str(name), "value": str(value)},
            _source=utils.Utils.get_database_path("local_settings.db"),
        )

        return {"data": "OK"}
    except Exception as error:
        log_error(str(error))
        return {"error": str(error)}
