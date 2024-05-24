import os
import logging
from dataclasses import dataclass, field
from typing import Any

from src.onvif.onvif_client import OnvifClient, OnvifClientServiceError, async_timeout_checker


@dataclass
class VideoResolution:
    width: int | None = None
    height: int | None = None


@dataclass
class RateControl:
    frame_rate_limit: float | None = None
    bitrate_limit: int | None = None
    constant_bitrate: bool | None = None


@dataclass
class Address:
    type: str | None = None
    ipv4_address: str | None = None
    ipv6_address: str | None = None


@dataclass
class Multicast:
    address: Address | None = None
    port: int | None = None
    ttl: int | None = None
    auto_start: bool | None = None


@dataclass
class VideoEncoderConfiguration:
    name: str | None = None
    use_count: int | None = None
    encoding: str | None = None
    resolution: VideoResolution | None = None
    rate_control: RateControl | None = None
    multicast: Multicast | None = None
    quality: float | None = None
    token: str | None = None
    gov_length: int | None = None
    profile: str | None = None
    guaranteed_frame_rate: float | None = None


@dataclass
class GetVideoEncoderConfigurationsResponse:
    encoders: list[VideoEncoderConfiguration] = field(default_factory=list)

    @staticmethod
    def create(obj: Any) -> "GetVideoEncoderConfigurationsResponse":
        return GetVideoEncoderConfigurationsResponse(
            encoders=[
                VideoEncoderConfiguration(
                    name=encoder["Name"],
                    use_count=encoder["UseCount"],
                    encoding=encoder["Encoding"],
                    resolution=VideoResolution(
                        width=encoder["Resolution"]["Width"],
                        height=encoder["Resolution"]["Height"],
                    ),
                    rate_control=RateControl(
                        frame_rate_limit=encoder["RateControl"]["FrameRateLimit"],
                        bitrate_limit=encoder["RateControl"]["BitrateLimit"],
                        constant_bitrate=encoder["RateControl"]["ConstantBitRate"],
                    ),
                    multicast=Multicast(
                        address=Address(
                            type=encoder["Multicast"]["Address"]["Type"],
                            ipv4_address=encoder["Multicast"]["Address"]["IPv4Address"],
                            ipv6_address=encoder["Multicast"]["Address"]["IPv6Address"],
                        ),
                        port=encoder["Multicast"]["Port"],
                        ttl=encoder["Multicast"]["TTL"],
                        auto_start=encoder["Multicast"]["AutoStart"],
                    ),
                    quality=encoder["Quality"],
                    token=encoder["token"],
                    gov_length=encoder["GovLength"],
                    profile=encoder["Profile"],
                    guaranteed_frame_rate=encoder["GuaranteedFrameRate"],
                )
                for encoder in obj
            ]
        )


class OnvifClientMedia2(OnvifClient):  # pylint: disable=too-few-public-methods
    BINDING_NAME = "{http://www.onvif.org/ver20/media/wsdl}Media2Binding"

    def _get_service_url(self):
        service_url = f"{self._get_base_url()}/onvif/media_service"
        logging.info("MediaService URL: %s", service_url)
        return service_url

    def _get_wsdl_path(self):
        return os.path.join(self.common.wsdl_path, "ver20/media/wsdl/media.wsdl")

    @async_timeout_checker
    async def get_video_encoder_configurations(self) -> GetVideoEncoderConfigurationsResponse:
        if not self.service:
            raise OnvifClientServiceError("Service doesn't initialized")
        resp = await self.service.GetVideoEncoderConfigurations()
        return GetVideoEncoderConfigurationsResponse.create(resp)
