import os
import logging
from dataclasses import dataclass

from src.onvif.onvif_client import OnvifClient, OnvifClientServiceError, async_timeout_checker


@dataclass
class AudioOutput:
    token: str = ""


@dataclass
class AudioOutputs:
    audio_outputs: list[AudioOutput]


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
        if not self.service:
            raise OnvifClientServiceError("Service doesn't initialized")
        resp = await self.service.GetAudioOutputs()
        return AudioOutputs(audio_outputs=[AudioOutput(token=audio["token"]) for audio in resp])
