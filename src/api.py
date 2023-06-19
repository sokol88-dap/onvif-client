import os
import logging

from fastapi import FastAPI, HTTPException

from src.model.source import Source
from src.config import ONVIFSettings
from src.onvif.onvif_client import OnvifClientSettings
from src.onvif.onvif_client_device import OnvifClientDevice, DeviceInfo
from src.onvif.onvif_client_media import OnvifClientMedia, AudioOutputs

logging.basicConfig(
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    level=os.environ.get("LOGGING", "INFO"),
)

app = FastAPI()


@app.post("/api/device/device_information")
async def get_device_information(source: Source) -> DeviceInfo:
    try:
        client = OnvifClientDevice(
            settings=OnvifClientSettings(source=source, common=ONVIFSettings())
        )
        return await client.get_device_information()
    except Exception as exc:  # pylint: disable=broad-except
        logging.exception("Error %s, Traceback: %s", exc, exc.__traceback__)
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.post("/api/media/get_audio_outputs")
async def get_audio_outputs(source: Source) -> AudioOutputs:
    try:
        client = OnvifClientMedia(
            settings=OnvifClientSettings(source=source, common=ONVIFSettings())
        )
        return await client.get_audio_outputs()
    except Exception as exc:  # pylint: disable=broad-except
        logging.exception("Error %s, Traceback: %s", exc, exc.__traceback__)
        raise HTTPException(status_code=409, detail=str(exc)) from exc
