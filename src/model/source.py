from pydantic import BaseModel, Field


class Source(BaseModel):
    host: str = Field(
        None,
        title="Camera host",
        description="It can be dns name or ip to the camera.",
        example="127.0.0.1",
    )
    port: int | None = Field(
        None,
        title="Camera port",
        description=(
            "Port for communication with camera by onvif. "
            "If it is None, then default port will be used."
        ),
        example=80,
    )
    user: str | None = Field(
        None,
        title="Camera user",
        description="User for authentication on the camera.",
        example="admin",
    )
    password: str | None = Field(
        None,
        title="Camera password",
        description="Password for authentication on the camera.",
        example="password",
    )
    bosch_security_url: str = Field(
        None,
        title="Bosch security url",
        description="Used when we try to connect to camera through Bosch security system.",
        example="https://cbs.com/rest/vx/v1/devices/bvip2:cb80a4b7569d/connection",
    )
