from pydantic import BaseSettings, BaseModel


class ONVIFSettings(BaseModel):
    wsdl_path: str = "src/wsdl/"
    timeout: int = 60
    operation_timeout: int = 60
    verify_ssl: bool = False


class CommonSettings(BaseSettings):
    onvif_settings: ONVIFSettings = ONVIFSettings()

    class Config:  # pylint: disable=too-few-public-methods
        env_nested_delimiter = "__"
        env_file = ".env"
        env_file_encoding = "utf-8"
