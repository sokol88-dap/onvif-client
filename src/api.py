import os
import logging

from fastapi import FastAPI

from src.model.source import Source
from src.config import ONVIFSettings
from src.onvif.onvif_client import OnvifClientSettings
from src.onvif.onvif_client_device import OnvifClientDevice, DeviceInfo

logging.basicConfig(
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    level=os.environ.get("LOGGING", "INFO"),
)

app = FastAPI()


@app.post("/api/v1/device_information")
async def get_device_information(source: Source) -> DeviceInfo:
    client = OnvifClientDevice(settings=OnvifClientSettings(source=source, common=ONVIFSettings()))
    return await client.get_device_information()
