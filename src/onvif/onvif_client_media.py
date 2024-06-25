import os
import logging
from dataclasses import dataclass
from enum import Enum

from src.onvif.onvif_client import OnvifClient, async_timeout_checker


@dataclass
class AudioOutput:
    token: str = ""


@dataclass
class AudioOutputs:
    audio_outputs: list[AudioOutput]


@dataclass
class Bounds:
    x: int | None = None
    y: int | None = None
    width: int | None = None
    height: int | None = None


class RotateMode(Enum):
    OFF = "OFF"
    ON = "ON"
    AUTO = "AUTO"


@dataclass
class Rotate:
    mode: RotateMode | None = None
    degree: int | None = None
    extension: dict | None = None


@dataclass
class LensOffset:
    x: float | None = None
    y: float | None = None


@dataclass
class LensProjection:
    angle: float | None = None
    radius: float | None = None
    transmittance: float | None = None


@dataclass
class LensDescription:
    focal_length: float | None = None
    offset: LensOffset | None = None
    projection: LensProjection | None = None
    x_factor: float | None = None


class SceneOrientationMode(Enum):
    MANUAL = "MANUAL"
    AUTO = "AUTO"


@dataclass
class SceneOrientation:
    mode: SceneOrientationMode | None = None
    orientation: str | None = None


@dataclass
class VideoSourceConfigurationExtension2:
    lens_description: LensDescription | None = None
    scene_orientation: SceneOrientation | None = None


@dataclass
class VideoSourceConfigurationExtension:
    rotate: Rotate = Rotate()
    extension: VideoSourceConfigurationExtension2 = VideoSourceConfigurationExtension2()


@dataclass
class VideoSourceConfiguration:
    token: str = ""
    name: str = ""
    use_count: int = 0
    view_mode: str = ""
    source_token: str = ""
    bounds: Bounds = Bounds()
    extension: VideoSourceConfigurationExtension = VideoSourceConfigurationExtension()


@dataclass
class MediaProfile:
    token: str = ""
    fixed: bool = False
    name: str = ""
    video_source_configuration: VideoSourceConfiguration = VideoSourceConfiguration()


@dataclass
class MediaProfiles:
    profiles: list[MediaProfile]


class OnvifClientMedia(OnvifClient):  # pylint: disable=too-few-public-methods
    BINDING_NAME = "{http://www.onvif.org/ver10/media/wsdl}MediaBinding"

    def _get_service_url(self):
        service_url = f"{self._get_base_url()}/onvif/media_service"
        logging.info("MediaService URL: %s", service_url)
        return service_url

    def _get_wsdl_path(self):
        return os.path.join(self.common.wsdl_path, "ver10/media/wsdl/media.wsdl")

    @async_timeout_checker
    async def get_audio_outputs(self) -> AudioOutputs:
        self._check_service()
        resp = await self.service.GetAudioOutputs()  # type: ignore
        return AudioOutputs(audio_outputs=[AudioOutput(token=audio["token"]) for audio in resp])

    @async_timeout_checker
    async def get_profiles(self) -> dict[str, str]:
        self._check_service()
        resp = await self.service.GetProfiles()  # type: ignore
        logging.info("Profiles: %s", resp)
        return {"test": "test"}
