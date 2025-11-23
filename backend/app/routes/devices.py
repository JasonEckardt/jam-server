from app import db
from app.api import spotify
from app.models.queue import Queue
from flask import Blueprint
import config.spotify_urls as urls

devices = Blueprint("devices", __name__)


@devices.route("/devices")
def list_devices():
    devices_response, status = spotify.request_api(
        urls.DEVICES, headers=urls.get_headers()
    )
    return devices_response, status


@devices.route("/devices/select/<string:id>", methods=["POST"])
def devices_select(id: str) -> dict:
    devices_response = spotify.request_api(urls.DEVICES, headers=urls.get_headers())

    devices_list = devices_response.get("devices", [])
    if not devices_list:
        return {"error": "Error getting devices."}, 400

    device_select = next((d for d in devices_list if d["id"] == id), None)
    if not device_select:
        return {"error": f"Device {id} not found."}, 404

    queue = db.session.get(Queue, "main")
    queue.active_device = device_select["id"]
    db.session.commit()

    return device_select
