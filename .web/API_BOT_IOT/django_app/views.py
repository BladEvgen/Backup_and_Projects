import datetime
import json

from django.db.models import F
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import utils
from .models import Device, DeviceData


@api_view(["POST"])
def get_params_api(request):
    try:
        payload = json.loads(request.body)
        data_list = payload.get("message", [])
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    device_data_list = []

    for data in data_list:
        device_id = data.get("serial_id")
        device, created = Device.objects.get_or_create(device_id=device_id)

        device_data = DeviceData(
            device=device,
            x=data.get("x"),
            y=data.get("y"),
            is_working=data.get("is_working"),
            fuel=data.get("fuel"),
            speed=data.get("speed"),
            device_time=datetime.datetime.strptime(
                str(data.get("device_time")), "%Y-%m-%d %H:%M:%S"
            )
            + datetime.timedelta(hours=6),
        )
        device_data_list.append(device_data)

    DeviceData.objects.bulk_create(device_data_list)
    return Response(
        {"message": "Data received successfully"}, status=status.HTTP_201_CREATED
    )


@api_view(["GET"])
def sent_message_api(request):
    not_in_network_data = utils.check_device_status()
    no_network_device_ids = set(
        device_info["id"] for device_info in not_in_network_data
    )

    all_data = (
        DeviceData.objects.exclude(device_id__in=no_network_device_ids)
        .annotate(device_id_actual=F("device__device_id"))
        .values()
    )

    response_data = {
        "no_network_data": not_in_network_data,
        "data": list(all_data),
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(http_method_names=["GET", "POST", "PUT", "PATCH", "DELETE"])
def api(request):
    return Response(data={"message": "OK"})


def home(request):
    return JsonResponse(data={"message": "Home OK"})
