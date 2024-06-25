import os
import logging
from functools import wraps

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
from src.onvif.onvif_client_replay import OnvifClientReplay


logging.basicConfig(
    format="%(asctime)s %(filename)s %(levelname)s: %(message)s",
    level=os.environ.get("LOGGING", "INFO"),
)

app = FastAPI()
device_router = APIRouter()
media_router = APIRouter()
media2_router = APIRouter()
replay_router = APIRouter()


def conflict_exception_decorator(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as exc:  # pylint: disable=broad-except
            logging.exception("Error %s, Traceback: %s", exc, exc.__traceback__)
            raise HTTPException(status_code=409, detail=str(exc)) from exc

    return wrapper


@device_router.post("/get_device_information", tags=["Device"])
@conflict_exception_decorator
async def get_device_information(source: Source) -> DeviceInformation:
    client = OnvifClientDevice(settings=OnvifClientSettings(source=source, common=ONVIFSettings()))
    return await client.get_device_information()


@device_router.post("/get_system_date_and_time", tags=["Device"])
@conflict_exception_decorator
async def get_system_date_and_time(source: Source) -> SystemDateTime:
    client = OnvifClientDevice(settings=OnvifClientSettings(source=source, common=ONVIFSettings()))
    return await client.get_system_date_and_time()


@device_router.post("/get_system_uris", tags=["Device"])
@conflict_exception_decorator
async def get_system_uris(source: Source) -> SystemUris:
    client = OnvifClientDevice(settings=OnvifClientSettings(source=source, common=ONVIFSettings()))
    return await client.get_system_uris()


@media_router.post("/get_audio_outputs", tags=["Media"])
@conflict_exception_decorator
async def get_audio_outputs(source: Source) -> AudioOutputs:
    client = OnvifClientMedia(settings=OnvifClientSettings(source=source, common=ONVIFSettings()))
    return await client.get_audio_outputs()


@media_router.post("/get_profiles", tags=["Media"])
@conflict_exception_decorator
async def get_profiles(source: Source) -> dict[str, str]:
    client = OnvifClientMedia(settings=OnvifClientSettings(source=source, common=ONVIFSettings()))
    return await client.get_profiles()


@media2_router.post("/get_video_encoder_configurations", tags=["Media2"])
@conflict_exception_decorator
async def get_video_encoder_configurations(source: Source) -> GetVideoEncoderConfigurationsResponse:
    client = OnvifClientMedia2(settings=OnvifClientSettings(source=source, common=ONVIFSettings()))
    return await client.get_video_encoder_configurations()


@media_router.post("/get_profiles_2", tags=["Media2"])
@conflict_exception_decorator
async def get_profiles_2(source: Source) -> dict[str, str]:
    client = OnvifClientMedia2(settings=OnvifClientSettings(source=source, common=ONVIFSettings()))
    return await client.get_profiles()


@replay_router.post("/get_replay_uri", tags=["Replay"])
@conflict_exception_decorator
async def get_replay_uri(source: Source) -> dict[str, str]:
    client = OnvifClientReplay(settings=OnvifClientSettings(source=source, common=ONVIFSettings()))
    return await client.get_replay_uri()


app.include_router(device_router, prefix="/api/device")
app.include_router(media_router, prefix="/api/media")
app.include_router(media2_router, prefix="/api/media2")
app.include_router(replay_router, prefix="/api/replay")
