import os
import logging

from fastapi import FastAPI, HTTPException, APIRouter

from src.model.source import Source
from src.config import ONVIFSettings
from src.onvif.onvif_client import OnvifClientSettings
from src.onvif.onvif_client_device import (
    OnvifClientDevice,
    DeviceInformation,
    SystemDateTime,
    SystemUris,
)
from src.onvif.onvif_client_media import OnvifClientMedia, AudioOutputs
from src.onvif.onvif_client_media_2 import OnvifClientMedia2, GetVideoEncoderConfigurationsResponse

logging.basicConfig(
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    level=os.environ.get("LOGGING", "INFO"),
)

app = FastAPI()
device_router = APIRouter()
media_router = APIRouter()
media2_router = APIRouter()


@device_router.post("/get_device_information", tags=["Device"])
async def get_device_information(source: Source) -> DeviceInformation:
    try:
        client = OnvifClientDevice(
            settings=OnvifClientSettings(source=source, common=ONVIFSettings())
        )
        return await client.get_device_information()
    except Exception as exc:  # pylint: disable=broad-except
        logging.exception("Error %s, Traceback: %s", exc, exc.__traceback__)
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@device_router.post("/get_system_date_and_time", tags=["Device"])
async def get_system_date_and_time(source: Source) -> SystemDateTime:
    try:
        client = OnvifClientDevice(
            settings=OnvifClientSettings(source=source, common=ONVIFSettings())
        )
        return await client.get_system_date_and_time()
    except Exception as exc:  # pylint: disable=broad-except
        logging.exception("Error %s, Traceback: %s", exc, exc.__traceback__)
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@device_router.post("/get_system_uris", tags=["Device"])
async def get_system_uris(source: Source) -> SystemUris:
    try:
        client = OnvifClientDevice(
            settings=OnvifClientSettings(source=source, common=ONVIFSettings())
        )
        return await client.get_system_uris()
    except Exception as exc:  # pylint: disable=broad-except
        logging.exception("Error %s, Traceback: %s", exc, exc.__traceback__)
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@media_router.post("/get_audio_outputs", tags=["Media"])
async def get_audio_outputs(source: Source) -> AudioOutputs:
    try:
        client = OnvifClientMedia(
            settings=OnvifClientSettings(source=source, common=ONVIFSettings())
        )
        return await client.get_audio_outputs()
    except Exception as exc:  # pylint: disable=broad-except
        logging.exception("Error %s, Traceback: %s", exc, exc.__traceback__)
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@media2_router.post("/get_video_encoder_configurations", tags=["Media2"])
async def get_video_encoder_configurations(source: Source) -> GetVideoEncoderConfigurationsResponse:
    try:
        client = OnvifClientMedia2(
            settings=OnvifClientSettings(source=source, common=ONVIFSettings())
        )
        return await client.get_video_encoder_configurations()
    except Exception as exc:  # pylint: disable=broad-except
        logging.exception("Error %s, Traceback: %s", exc, exc.__traceback__)
        raise HTTPException(status_code=409, detail=str(exc)) from exc


app.include_router(device_router, prefix="/api/device")
app.include_router(media_router, prefix="/api/media")
app.include_router(media2_router, prefix="/api/media2")
