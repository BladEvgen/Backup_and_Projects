import datetime
from . import models


def check_device_status():
    current_time = datetime.datetime.now()
    devices_not_in_network = []

    for device in models.Device.objects.all():
        last_data = (
            models.DeviceData.objects.filter(device=device)
            .order_by("-device_time")
            .first()
        )

        if last_data:
            time_difference = current_time - last_data.device_time.replace(tzinfo=None)
            if (
                time_difference.total_seconds() > 300
                and last_data.device_time.date() == current_time.date()
            ):
                device_info = {
                    "id": device.id,
                    "device_id": device.device_id,
                    "last_seen_time": last_data.device_time.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                }
                devices_not_in_network.append(device_info)

    return devices_not_in_network
