"""Base class for onvif clients"""
from abc import abstractmethod
from dataclasses import dataclass
from functools import wraps

import httpx
from httpx import ReadTimeout, ConnectTimeout  # we used httpx inside of zeep
from zeep import Settings, AsyncClient
from zeep.proxy import ServiceProxy, AsyncServiceProxy
from zeep.wsse.username import UsernameToken
from zeep.transports import AsyncTransport

from src.config import ONVIFSettings
from src.model.source import Source


@dataclass
class OnvifClientSettings:
    source: Source
    common: ONVIFSettings


class CreateOnvifClientError(Exception):
    pass


class OnvifClientServiceError(Exception):
    pass


class ReadTimeoutAsyncOnvifClientError(Exception):
    pass


def async_timeout_checker(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (ReadTimeout, ConnectTimeout) as exc:
            raise OnvifClientServiceError("ONVIF timeout error") from exc

    return wrapper


def get_camera_url_for_bosch_security(url):
    response = httpx.post(url, verify=False, timeout=30)
    response.raise_for_status()
    return response.json()["onvifUrl"].replace("/onvif/device_service", "")


class AsyncZeepClientFix(AsyncClient):
    """
    This class need to workaround issue with Exception:
    AttributeError: 'coroutine' object has no attribute 'status_code'.
    This issue is described here:
    https://github.com/mvantellingen/python-zeep/issues/1168
    https://github.com/mvantellingen/python-zeep/issues/1288
    Currently this project has no solution for this issue but it's doesn't merged yet.
    So we need to use this workaround.
    """

    def create_service(self, binding_name: str, address: str) -> AsyncServiceProxy:
        """Create a new AsyncServiceProxy for the given binding name and address.

        :param binding_name: The QName of the binding
        :param address: The address of the endpoint

        """
        try:
            binding = self.wsdl.bindings[binding_name]
        except KeyError as exc:
            raise ValueError(
                f"No binding found with the given QName. Available bindings "
                f"are: {', '.join(self.wsdl.bindings.keys())}"
            ) from exc
        return AsyncServiceProxy(self, binding, address=address)


class OnvifClient:  # pylint: disable=too-few-public-methods
    BINDING_NAME = ""

    def __init__(self, settings: OnvifClientSettings) -> None:
        self.source: Source = settings.source
        self.common: ONVIFSettings = settings.common
        self.service: ServiceProxy | None = self._get_service()

    def _get_service(self) -> AsyncServiceProxy | None:
        if client := self._create_client():
            return client.create_service(self.BINDING_NAME, self._get_service_url())
        raise CreateOnvifClientError("We couldn't create onvif client")

    def _create_client(self) -> AsyncClient:
        return AsyncZeepClientFix(
            wsdl=self._get_wsdl_path(),
            wsse=UsernameToken(self.source.user or "", self.source.password or "", use_digest=True),
            settings=Settings(xml_huge_tree=True, raw_response=False, strict=False),
            transport=AsyncTransport(
                timeout=self.common.timeout, operation_timeout=self.common.operation_timeout
            ),
        )

    def _get_base_url(self):
        if self.source.bosch_security_url:
            return get_camera_url_for_bosch_security(self.source.bosch_security_url)
        return f"http://{self.source.host}:{self.source.port}"

    @abstractmethod
    def _get_service_url(self):
        pass

    @abstractmethod
    def _get_wsdl_path(self):
        pass
