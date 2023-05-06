import os
from dataclasses import dataclass

from src.onvif.onvif_client import OnvifClient, OnvifClientServiceError, async_timeout_checker


@dataclass
class DeviceInfo:
    manufacturer: str = ""
    model: str = ""
    firmware_version: str = ""
    serial_number: str = ""
    hardware_id: str = ""


class OnvifClientDeviceWrongTimezone(Exception):
    pass


class OnvifClientDeviceWrongInformation(Exception):
    pass


class OnvifClientDevice(OnvifClient):  # pylint: disable=too-few-public-methods
    BINDING_NAME = "{http://www.onvif.org/ver10/device/wsdl}DeviceBinding"

    def _get_service_url(self):
        if self.source.is_tunnel:
            return f"{self.source.host}/onvif/device_service"
        return f"http://{self.source.host}:{self.source.port}/onvif/device_service"

    def _get_wsdl_path(self):
        # return os.path.join(self.common.wsdl_path, "ver10/device/wsdl/devicemgmt.wsdl")
        return os.path.join(self.common.wsdl_path, "devicemgmt.wsdl")

    @async_timeout_checker
    async def get_device_information(self) -> DeviceInfo:
        if not self.service:
            raise OnvifClientServiceError("Service doesn't initialized")
        resp = await self.service.GetDeviceInformation()
        return DeviceInfo(
            manufacturer=resp["Manufacturer"],
            model=resp["Model"],
            firmware_version=resp["FirmwareVersion"],
            serial_number=resp["SerialNumber"],
            hardware_id=resp["HardwareId"],
        )
