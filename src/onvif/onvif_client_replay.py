import os
import logging

from src.onvif.onvif_client import OnvifClient, async_timeout_checker


class OnvifClientReplay(OnvifClient):  # pylint: disable=too-few-public-methods
    BINDING_NAME = "{http://www.onvif.org/ver10/replay/wsdl}ReplayBinding"

    def _get_service_url(self):
        # service_url = f"{self._get_base_url()}/onvif/replay_service"
        service_url = f"{self._get_base_url()}/onvif/Replay"  # Homaxi used another URL
        logging.info("ReplayService URL: %s", service_url)
        return service_url

    def _get_wsdl_path(self):
        return os.path.join(self.common.wsdl_path, "ver10/replay.wsdl")

    @async_timeout_checker
    async def get_replay_uri(self) -> dict[str, str]:
        self._check_service()
        resp = await self.service.GetReplayUri(  # type: ignore
            StreamSetup={"Stream": "RTP-Unicast", "Transport": {"Protocol": "UDP"}},
            RecordingToken="OnvifRecordingToken_1",
        )
        logging.info("GetReplayUri: %s", resp)
        return {"test": "test"}
