import os
from dataclasses import dataclass
from typing import Any

from src.onvif.onvif_client import OnvifClient, OnvifClientServiceError, async_timeout_checker


@dataclass
class DeviceInformation:
    manufacturer: str
    model: str
    firmware_version: str
    serial_number: str
    hardware_id: str

    @staticmethod
    def create(obj: Any) -> "DeviceInformation":
        return DeviceInformation(
            manufacturer=obj["Manufacturer"],
            model=obj["Model"],
            firmware_version=obj["FirmwareVersion"],
            serial_number=obj["SerialNumber"],
            hardware_id=obj["HardwareId"],
        )


@dataclass
class Time:
    hour: int
    minute: int
    second: int

    @staticmethod
    def create(obj: Any) -> "Time":
        return Time(hour=obj["Hour"], minute=obj["Minute"], second=obj["Second"])


@dataclass
class Date:
    year: int
    month: int
    day: int

    @staticmethod
    def create(obj: Any) -> "Date":
        return Date(year=obj["Year"], month=obj["Month"], day=obj["Day"])


@dataclass
class DateTime:
    time: Time
    date: Date

    @staticmethod
    def create(obj: Any) -> "DateTime":
        return DateTime(time=Time.create(obj["Time"]), date=Date.create(obj["Date"]))


@dataclass
class SystemDateTime:
    date_time_type: str | None = None
    daylight_savings: bool | None = None
    time_zone: str | None = None
    utc_date_time: DateTime | None = None
    local_date_time: DateTime | None = None
    extension: dict | None = None

    @staticmethod
    def create(obj: Any) -> "SystemDateTime":
        return SystemDateTime(
            date_time_type=obj["DateTimeType"],
            daylight_savings=obj["DaylightSavings"],
            time_zone=obj["TimeZone"]["TZ"],
            utc_date_time=DateTime.create(obj["UTCDateTime"]) if obj["UTCDateTime"] else None,
            local_date_time=DateTime.create(obj["LocalDateTime"]) if obj["LocalDateTime"] else None,
            extension=obj["Extension"],
        )


class OnvifClientDevice(OnvifClient):  # pylint: disable=too-few-public-methods
    BINDING_NAME = "{http://www.onvif.org/ver10/device/wsdl}DeviceBinding"

    def _get_service_url(self):
        return f"{self._get_base_url()}/onvif/device_service"

    def _get_wsdl_path(self):
        return os.path.join(self.common.wsdl_path, "ver10/device/wsdl/devicemgmt.wsdl")

    @async_timeout_checker
    async def get_device_information(self) -> DeviceInformation:
        if not self.service:
            raise OnvifClientServiceError("Service doesn't initialized")
        resp = await self.service.GetDeviceInformation()
        return DeviceInformation.create(resp)

    @async_timeout_checker
    async def get_system_date_and_time(self) -> SystemDateTime:
        if not self.service:
            raise OnvifClientServiceError("Service doesn't initialized")
        resp = await self.service.GetSystemDateAndTime()
        return SystemDateTime.create(resp)
