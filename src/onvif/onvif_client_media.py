import os
from dataclasses import dataclass
from enum import Enum
from typing import Any

from src.onvif.onvif_client import OnvifClient, async_timeout_checker


@dataclass
class AudioOutput:
    token: str = ""

    @staticmethod
    def create(obj: Any) -> "AudioOutput":
        return AudioOutput(token=obj["token"])


@dataclass
class AudioOutputs:
    audio_outputs: list[AudioOutput]

    @staticmethod
    def create(obj: Any) -> "AudioOutputs":
        return AudioOutputs(audio_outputs=[AudioOutput.create(audio) for audio in obj])


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


class VideoEncoding(Enum):
    JPEG = "JPEG"
    MPEG4 = "MPEG4"
    H264 = "H264"


class SceneOrientationMode(Enum):
    MANUAL = "MANUAL"
    AUTO = "AUTO"


class Mpeg4Profile(Enum):
    SP = "SP"
    ASP = "ASP"


class H264Profile(Enum):
    BASELINE = "Baseline"
    MAIN = "Main"
    EXTENDED = "Extended"
    HIGH = "High"


class IPType(Enum):
    IPV4 = "IPv4"
    IPV6 = "IPv6"


class EFlipMode(Enum):
    OFF = "OFF"
    ON = "ON"
    EXTENDED = "Extended"


class ReverseMode(Enum):
    OFF = "OFF"
    ON = "ON"
    AUTO = "AUTO"
    EXTENDED = "Extended"


class AudioEncoding(Enum):
    G711 = "G711"
    G726 = "G726"
    AAC = "AAC"


@dataclass
class VideoResolution:
    width: int
    height: int

    @staticmethod
    def create(obj: Any) -> "VideoResolution":
        return VideoResolution(width=obj["Width"], height=obj["Height"])


@dataclass
class Rotate:
    mode: RotateMode | None = None
    degree: int | None = None
    extension: dict | None = None

    @staticmethod
    def create(obj: Any) -> "Rotate":
        return Rotate(
            mode=RotateMode(obj["Mode"]), degree=obj["Degree"], extension=obj["Extension"]
        )


@dataclass
class LensOffset:
    x: float | None = None
    y: float | None = None

    @staticmethod
    def create(obj: Any) -> "LensOffset":
        return LensOffset(x=obj["x"], y=obj["y"])


@dataclass
class LensProjection:
    angle: float | None = None
    radius: float | None = None
    transmittance: float | None = None

    @staticmethod
    def create(obj: Any) -> "LensProjection":
        return LensProjection(
            angle=obj["Angle"],
            radius=obj["Radius"],
            transmittance=obj["Transmittance"],
        )


@dataclass
class LensDescription:
    focal_length: float | None = None
    offset: LensOffset | None = None
    projection: LensProjection | None = None
    x_factor: float | None = None

    @staticmethod
    def create(obj: Any) -> "LensDescription":
        offset = LensOffset.create(obj["Offset"]) if obj.get("Offset") else None
        projection = LensProjection.create(obj["Projection"]) if obj.get("Projection") else None
        return LensDescription(
            focal_length=obj["FocalLength"],
            offset=offset,
            projection=projection,
            x_factor=obj["XFactor"],
        )


@dataclass
class SceneOrientation:
    mode: SceneOrientationMode | None = None
    orientation: str | None = None

    @staticmethod
    def create(obj: Any) -> "SceneOrientation":
        return SceneOrientation(
            mode=SceneOrientationMode(obj["Mode"]), orientation=obj["Orientation"]
        )


@dataclass
class VideoSourceConfigurationExtension2:
    lens_description: LensDescription | None = None
    scene_orientation: SceneOrientation | None = None

    @staticmethod
    def create(obj: Any) -> "VideoSourceConfigurationExtension2":
        lens_description = (
            LensDescription.create(obj["LensDescription"]) if obj.get("LensDescription") else None
        )
        scene_orientation = (
            SceneOrientation.create(obj["SceneOrientation"])
            if obj.get("SceneOrientation")
            else None
        )
        return VideoSourceConfigurationExtension2(
            lens_description=lens_description, scene_orientation=scene_orientation
        )


@dataclass
class VideoSourceConfigurationExtension:
    rotate: Rotate | None = None
    extension: VideoSourceConfigurationExtension2 | None = None

    @staticmethod
    def create(obj: Any) -> "VideoSourceConfigurationExtension":
        rotate = Rotate.create(obj["Rotate"]) if obj["Rotate"] else None
        extension = (
            VideoSourceConfigurationExtension2.create(obj["Extension"])
            if obj["Extension"]
            else None
        )
        return VideoSourceConfigurationExtension(rotate=rotate, extension=extension)


@dataclass
class VideoRateControl:
    frame_rate_limit: int | None = None
    encoding_interval: int | None = None
    bitrate_limit: int | None = None

    @staticmethod
    def create(obj: Any) -> "VideoRateControl":
        return VideoRateControl(
            frame_rate_limit=obj["FrameRateLimit"],
            encoding_interval=obj["EncodingInterval"],
            bitrate_limit=obj["BitrateLimit"],
        )


@dataclass
class Mpeg4Configuration:
    gov_length: int
    mpeg4_profile: Mpeg4Profile

    @staticmethod
    def create(obj: Any) -> "Mpeg4Configuration":
        return Mpeg4Configuration(
            gov_length=obj["GovLength"], mpeg4_profile=Mpeg4Profile(obj["Mpeg4Profile"])
        )


@dataclass
class H264Configuration:
    gov_length: int
    h264_profile: H264Profile

    @staticmethod
    def create(obj: Any) -> "H264Configuration":
        return H264Configuration(
            gov_length=obj["GovLength"], h264_profile=H264Profile(obj["H264Profile"])
        )


@dataclass
class IPAddress:
    ip_type: IPType
    ipv4_address: str | None = None
    ipv6_address: str | None = None

    @staticmethod
    def create(obj: Any) -> "IPAddress":
        return IPAddress(
            ip_type=IPType(obj["Type"]),
            ipv4_address=obj["IPv4Address"] if obj["IPv4Address"] else None,
            ipv6_address=obj["IPv6Address"] if obj["IPv6Address"] else None,
        )


@dataclass
class MulticastConfiguration:
    address: IPAddress
    port: int
    ttl: int
    auto_start: bool

    @staticmethod
    def create(obj: Any) -> "MulticastConfiguration":
        return MulticastConfiguration(
            address=IPAddress.create(obj["Address"]),
            port=obj["Port"],
            ttl=obj["TTL"],
            auto_start=obj["AutoStart"],
        )


@dataclass
class VideoSourceConfiguration:
    token: str
    name: str
    use_count: int
    source_token: str
    view_mode: str | None = None
    bounds: Bounds | None = None
    extension: VideoSourceConfigurationExtension | None = None

    @staticmethod
    def create(obj: Any) -> "VideoSourceConfiguration":
        bounds = Bounds(
            x=obj["Bounds"]["x"],
            y=obj["Bounds"]["y"],
            width=obj["Bounds"]["width"],
            height=obj["Bounds"]["height"],
        )
        extension = (
            VideoSourceConfigurationExtension.create(obj["Extension"]) if obj["Extension"] else None
        )
        return VideoSourceConfiguration(
            token=obj["token"],
            name=obj["Name"],
            use_count=obj["UseCount"],
            view_mode=obj["ViewMode"] if obj["ViewMode"] else None,
            source_token=obj["SourceToken"],
            bounds=bounds,
            extension=extension,
        )


@dataclass
class AudioSourceConfiguration:
    token: str
    name: str
    use_count: int
    source_token: str

    @staticmethod
    def create(obj: Any) -> "AudioSourceConfiguration":
        return AudioSourceConfiguration(
            token=obj["token"],
            name=obj["Name"],
            use_count=obj["UseCount"],
            source_token=obj["SourceToken"],
        )


@dataclass
class VideoEncoderConfiguration:
    token: str
    name: str
    use_count: int
    encoding: VideoEncoding
    resolution: VideoResolution
    quality: float
    multicast: MulticastConfiguration
    session_timeout: str
    guaranteed_frame_rate: bool | None = None
    rate_control: VideoRateControl | None = None
    mpeg4: Mpeg4Configuration | None = None
    h264: H264Configuration | None = None

    @staticmethod
    def create(obj: Any) -> "VideoEncoderConfiguration":
        rate_control = VideoRateControl.create(obj["RateControl"]) if obj["RateControl"] else None
        mpeg4 = Mpeg4Configuration.create(obj["MPEG4"]) if obj["MPEG4"] else None
        h264 = H264Configuration.create(obj["H264"]) if obj["H264"] else None
        return VideoEncoderConfiguration(
            token=obj["token"],
            name=obj["Name"],
            use_count=obj["UseCount"],
            guaranteed_frame_rate=(
                obj["GuaranteedFrameRate"] if obj["GuaranteedFrameRate"] else None
            ),
            encoding=VideoEncoding(obj["Encoding"]),
            resolution=VideoResolution.create(obj["Resolution"]),
            quality=obj["Quality"],
            rate_control=rate_control,
            mpeg4=mpeg4,
            h264=h264,
            multicast=MulticastConfiguration.create(obj["Multicast"]),
            session_timeout=str(obj["SessionTimeout"]),
        )


@dataclass
class AudioEncoderConfiguration:
    token: str
    name: str
    use_count: int
    encoding: AudioEncoding
    bitrate: int
    sample_rate: int
    multicast: MulticastConfiguration
    session_timeout: str

    @staticmethod
    def create(obj: Any) -> "AudioEncoderConfiguration":
        return AudioEncoderConfiguration(
            token=obj["token"],
            name=obj["Name"],
            use_count=obj["UseCount"],
            encoding=AudioEncoding(obj["Encoding"]),
            bitrate=obj["Bitrate"],
            sample_rate=obj["SampleRate"],
            multicast=MulticastConfiguration.create(obj["Multicast"]),
            session_timeout=str(obj["SessionTimeout"]),
        )


@dataclass
class SimpleItem:
    name: str
    value: Any

    @staticmethod
    def create(obj: Any) -> "SimpleItem":
        return SimpleItem(name=obj["Name"], value=obj["Value"])


@dataclass
class ElementItem:
    name: str

    @staticmethod
    def create(obj: Any) -> "ElementItem":
        return ElementItem(name=obj["Name"])


@dataclass
class Parameter:
    simple_item: SimpleItem | None = None
    element_item: ElementItem | None = None
    extension: dict | None = None

    @staticmethod
    def create(obj: Any) -> "Parameter":
        simple_item = SimpleItem.create(obj["SimpleItem"][0]) if obj["SimpleItem"] else None
        element_item = ElementItem.create(obj["ElementItem"][0]) if obj["ElementItem"] else None
        return Parameter(
            simple_item=simple_item, element_item=element_item, extension=obj["Extension"]
        )


@dataclass
class Config:
    name: str | None
    type: str | None
    parameters: list[Parameter]

    @staticmethod
    def create(obj: Any) -> "Config":
        parameters = (
            obj["Parameters"] if isinstance(obj["Parameters"], list) else [obj["Parameters"]]
        )
        return Config(
            name=obj["Name"],
            type=obj["Type"],
            parameters=[Parameter.create(param) for param in parameters],
        )


@dataclass
class AnalyticsEngineConfiguration:
    analytics_module: list[Config] | None = None
    extension: dict | None = None

    @staticmethod
    def create(obj: Any) -> "AnalyticsEngineConfiguration":
        analytics_module = [Config.create(module) for module in obj["AnalyticsModule"]]
        return AnalyticsEngineConfiguration(
            analytics_module=analytics_module, extension=obj["Extension"]
        )


@dataclass
class RuleEngineConfiguration:
    rule: list[Config] | None = None
    extension: dict | None = None

    @staticmethod
    def create(obj: Any) -> "RuleEngineConfiguration":
        # rule = Config.create(obj["Rule"]) if obj["Rule"] else None
        rule = [Config.create(rule) for rule in obj["Rule"]] if obj["Rule"] else None
        return RuleEngineConfiguration(rule=rule, extension=obj["Extension"])


@dataclass
class VideoAnalyticsConfiguration:
    token: str
    name: str
    use_count: int
    analytics_engine_configuration: AnalyticsEngineConfiguration
    rule_engine_configuration: RuleEngineConfiguration

    @staticmethod
    def create(obj: Any) -> "VideoAnalyticsConfiguration":
        return VideoAnalyticsConfiguration(
            token=obj["token"],
            name=obj["Name"],
            use_count=obj["UseCount"],
            analytics_engine_configuration=AnalyticsEngineConfiguration.create(
                obj["AnalyticsEngineConfiguration"]
            ),
            rule_engine_configuration=RuleEngineConfiguration.create(
                obj["RuleEngineConfiguration"]
            ),
        )


@dataclass
class PTZSpeed:
    pan_tilt: float
    zoom: float

    @staticmethod
    def create(obj: Any) -> "PTZSpeed":
        return PTZSpeed(pan_tilt=obj["PanTilt"], zoom=obj["Zoom"])


@dataclass
class FloatRange:
    min: float
    max: float

    @staticmethod
    def create(obj: Any) -> "FloatRange":
        return FloatRange(min=obj["Min"], max=obj["Max"])


@dataclass
class Space2DDescription:
    uri: str
    x_range: FloatRange
    y_range: FloatRange
    extension: dict | None = None

    @staticmethod
    def create(obj: Any) -> "Space2DDescription":
        return Space2DDescription(
            uri=obj["URI"],
            x_range=FloatRange.create(obj["XRange"]),
            y_range=FloatRange.create(obj["YRange"]),
            extension=obj["Extension"],
        )


@dataclass
class Space1DDescription:
    uri: str
    x_range: FloatRange

    @staticmethod
    def create(obj: Any) -> "Space1DDescription":
        return Space1DDescription(uri=obj["URI"], x_range=FloatRange.create(obj["XRange"]))


@dataclass
class PanTiltLimits:
    range: Space2DDescription

    @staticmethod
    def create(obj: Any) -> "PanTiltLimits":
        return PanTiltLimits(range=Space2DDescription.create(obj["Range"]))


@dataclass
class ZoomLimits:
    range: Space1DDescription

    @staticmethod
    def create(obj: Any) -> "ZoomLimits":
        return ZoomLimits(range=Space1DDescription.create(obj["Range"]))


@dataclass
class EFlip:
    mode: EFlipMode | None = None

    @staticmethod
    def create(obj: Any) -> "EFlip":
        return EFlip(mode=EFlipMode(obj["Mode"]))


@dataclass
class Reverse:
    mode: ReverseMode | None = None

    @staticmethod
    def create(obj: Any) -> "Reverse":
        return Reverse(mode=ReverseMode(obj["Mode"]))


@dataclass
class PTControlDirection:
    e_flip: EFlip | None = None
    reverse: Reverse | None = None
    extension: dict | None = None

    @staticmethod
    def create(obj: Any) -> "PTControlDirection":
        e_flip = EFlip.create(obj["EFlip"]) if obj.get("EFlip") else None
        reverse = Reverse.create(obj["Reverse"]) if obj.get("Reverse") else None
        return PTControlDirection(e_flip=e_flip, reverse=reverse, extension=obj["Extension"])


@dataclass
class PTZConfigurationExtension:
    pt_control_direction: PTControlDirection | None = None
    extension: dict | None = None

    @staticmethod
    def create(obj: Any) -> "PTZConfigurationExtension":
        pt_control_direction = (
            PTControlDirection.create(obj["PTControlDirection"])
            if obj.get("PTControlDirection")
            else None
        )
        return PTZConfigurationExtension(
            pt_control_direction=pt_control_direction, extension=obj["Extension"]
        )


@dataclass
class PTZConfiguration:
    token: str
    name: str
    use_count: int
    node_token: str
    default_ptz_timeout: float
    move_ramp: int | None = None
    preset_ramp: int | None = None
    preset_tour_ramp: int | None = None
    default_absolute_pant_tilt_position_space: str | None = None
    default_absolute_zoom_position_space: str | None = None
    default_relative_pan_tilt_translation_space: str | None = None
    default_relative_zoom_translation_space: str | None = None
    default_continuous_pan_tilt_velocity_space: str | None = None
    default_continuous_zoom_velocity_space: str | None = None
    default_ptz_speed: PTZSpeed | None = None
    pan_tilt_limits: PanTiltLimits | None = None
    zoom_limits: ZoomLimits | None = None
    extension: PTZConfigurationExtension | None = None

    @staticmethod
    def create(obj: Any) -> "PTZConfiguration":
        pan_tilt_limits = (
            PanTiltLimits.create(obj["PanTiltLimits"]) if obj["PanTiltLimits"] else None
        )
        zoom_limits = ZoomLimits.create(obj["ZoomLimits"]) if obj["ZoomLimits"] else None
        extension = PTZConfigurationExtension.create(obj["Extension"]) if obj["Extension"] else None
        return PTZConfiguration(
            token=obj["token"],
            name=obj["Name"],
            use_count=obj["UseCount"],
            move_ramp=obj["MoveRamp"],
            preset_ramp=obj["PresetRamp"],
            preset_tour_ramp=obj["PresetTourRamp"],
            node_token=obj["NodeToken"],
            default_absolute_pant_tilt_position_space=obj["DefaultAbsolutePantTiltPositionSpace"],
            default_absolute_zoom_position_space=obj["DefaultAbsoluteZoomPositionSpace"],
            default_relative_pan_tilt_translation_space=obj[
                "DefaultRelativePanTiltTranslationSpace"
            ],
            default_relative_zoom_translation_space=obj["DefaultRelativeZoomTranslationSpace"],
            default_continuous_pan_tilt_velocity_space=obj["DefaultContinuousPanTiltVelocitySpace"],
            default_continuous_zoom_velocity_space=obj["DefaultContinuousZoomVelocitySpace"],
            default_ptz_speed=(
                PTZSpeed.create(obj["DefaultPTZSpeed"]) if obj["DefaultPTZSpeed"] else None
            ),
            default_ptz_timeout=float(obj["DefaultPTZTimeout"].total_seconds()),
            pan_tilt_limits=pan_tilt_limits,
            zoom_limits=zoom_limits,
            extension=extension,
        )


@dataclass
class PTZFilter:
    status: bool
    position: bool

    @staticmethod
    def create(obj: Any) -> "PTZFilter":
        return PTZFilter(status=obj["Status"], position=obj["Position"])


@dataclass
class EventSubscription:
    filter: Any | None = None
    subscription_policy: Any | None = None

    @staticmethod
    def create(obj: Any) -> "EventSubscription":
        return EventSubscription(
            filter=obj["Filter"], subscription_policy=obj["SubscriptionPolicy"]
        )


@dataclass
class MetadataConfiguration:
    token: str
    name: str
    use_count: int
    compression_type: str
    geo_location: bool
    shape_polygon: bool
    session_timeout: str
    ptz_status: PTZFilter | None = None
    events: EventSubscription | None = None
    analytics: bool | None = None
    multicast: MulticastConfiguration | None = None
    analytics_engine_configuration: AnalyticsEngineConfiguration | None = None
    extension: Any | None = None

    @staticmethod
    def create(obj: Any) -> "MetadataConfiguration":
        ptz_status = PTZFilter.create(obj["PTZStatus"]) if obj.get("PTZStatus") else None
        events = EventSubscription.create(obj["Events"]) if obj.get("Events") else None
        multicast = (
            MulticastConfiguration.create(obj["Multicast"]) if obj.get("Multicast") else None
        )
        analytics_engine_configuration = (
            AnalyticsEngineConfiguration.create(obj["AnalyticsEngineConfiguration"])
            if obj.get("AnalyticsEngineConfiguration")
            else None
        )
        return MetadataConfiguration(
            token=obj["token"],
            name=obj["Name"],
            use_count=obj["UseCount"],
            compression_type=obj["CompressionType"],
            geo_location=obj["GeoLocation"],
            shape_polygon=obj["ShapePolygon"],
            ptz_status=ptz_status,
            events=events,
            analytics=obj["Analytics"],
            multicast=multicast,
            session_timeout=str(obj["SessionTimeout"]),
            analytics_engine_configuration=analytics_engine_configuration,
            extension=obj["Extension"],
        )


@dataclass
class AudioOutputConfiguration:
    token: str
    name: str
    use_count: int
    output_token: str
    output_level: int
    send_primacy: Any | None = None

    @staticmethod
    def create(obj: Any) -> "AudioOutputConfiguration":
        return AudioOutputConfiguration(
            token=obj["token"],
            name=obj["Name"],
            use_count=obj["UseCount"],
            output_token=obj["OutputToken"],
            send_primacy=obj["SendPrimacy"],
            output_level=obj["OutputLevel"],
        )


@dataclass
class AudioDecoderConfiguration:
    token: str
    name: str
    use_count: int

    @staticmethod
    def create(obj: Any) -> "AudioDecoderConfiguration":
        return AudioDecoderConfiguration(
            token=obj["token"], name=obj["Name"], use_count=obj["UseCount"]
        )


@dataclass
class ProfileExtension:
    audio_output_configuration: AudioOutputConfiguration | None = None
    audio_decoder_configuration: AudioDecoderConfiguration | None = None
    extension: Any | None = None

    @staticmethod
    def create(obj: Any) -> "ProfileExtension":
        audio_output_configuration = (
            AudioOutputConfiguration.create(obj["AudioOutputConfiguration"])
            if obj["AudioOutputConfiguration"]
            else None
        )
        audio_decoder_configuration = (
            AudioDecoderConfiguration.create(obj["AudioDecoderConfiguration"])
            if obj["AudioDecoderConfiguration"]
            else None
        )
        return ProfileExtension(
            audio_output_configuration=audio_output_configuration,
            audio_decoder_configuration=audio_decoder_configuration,
            extension=obj["Extension"],
        )


@dataclass
class MediaProfile:
    token: str = ""
    fixed: bool = False
    name: str = ""
    video_source_configuration: VideoSourceConfiguration | None = None
    audio_source_configuration: AudioSourceConfiguration | None = None
    video_encoder_configuration: VideoEncoderConfiguration | None = None
    audio_encoder_configuration: AudioEncoderConfiguration | None = None
    video_analytics_configuration: VideoAnalyticsConfiguration | None = None
    ptz_configuration: PTZConfiguration | None = None
    metadata_configuration: MetadataConfiguration | None = None
    extension: ProfileExtension | None = None

    @staticmethod
    def create(obj: Any) -> "MediaProfile":
        video_source_configuration = (
            VideoSourceConfiguration.create(obj["VideoSourceConfiguration"])
            if obj["VideoSourceConfiguration"]
            else None
        )
        audio_source_configuration = (
            AudioSourceConfiguration.create(obj["AudioSourceConfiguration"])
            if obj["AudioSourceConfiguration"]
            else None
        )
        video_encoder_configuration = (
            VideoEncoderConfiguration.create(obj["VideoEncoderConfiguration"])
            if obj["VideoEncoderConfiguration"]
            else None
        )
        audio_encoder_configuration = (
            AudioEncoderConfiguration.create(obj["AudioEncoderConfiguration"])
            if obj["AudioEncoderConfiguration"]
            else None
        )
        video_analytics_configuration = (
            VideoAnalyticsConfiguration.create(obj["VideoAnalyticsConfiguration"])
            if obj["VideoAnalyticsConfiguration"]
            else None
        )
        ptz_configuration = (
            PTZConfiguration.create(obj["PTZConfiguration"]) if obj["PTZConfiguration"] else None
        )
        metadata_configuration = (
            MetadataConfiguration.create(obj["MetadataConfiguration"])
            if obj["MetadataConfiguration"]
            else None
        )
        extension = ProfileExtension.create(obj["Extension"]) if obj["Extension"] else None
        return MediaProfile(
            token=obj["token"],
            fixed=obj["fixed"],
            name=obj["Name"],
            video_source_configuration=video_source_configuration,
            audio_source_configuration=audio_source_configuration,
            video_encoder_configuration=video_encoder_configuration,
            audio_encoder_configuration=audio_encoder_configuration,
            video_analytics_configuration=video_analytics_configuration,
            ptz_configuration=ptz_configuration,
            metadata_configuration=metadata_configuration,
            extension=extension,
        )


@dataclass
class MediaProfiles:
    profiles: list[MediaProfile]

    @staticmethod
    def create(obj: Any) -> "MediaProfiles":
        return MediaProfiles(profiles=[MediaProfile.create(profile) for profile in obj])


class OnvifClientMedia(OnvifClient):  # pylint: disable=too-few-public-methods
    BINDING_NAME = "{http://www.onvif.org/ver10/media/wsdl}MediaBinding"

    def _get_service_url(self):
        service_url = f"{self._get_base_url()}/onvif/media_service"
        return service_url

    def _get_wsdl_path(self):
        return os.path.join(self.common.wsdl_path, "ver10/media/wsdl/media.wsdl")

    @async_timeout_checker
    async def get_audio_outputs(self) -> AudioOutputs:
        self._check_service()
        resp = await self.service.GetAudioOutputs()  # type: ignore
        return AudioOutputs.create(resp)

    @async_timeout_checker
    async def get_profiles(self) -> MediaProfiles:
        self._check_service()
        resp = await self.service.GetProfiles()  # type: ignore
        return MediaProfiles.create(resp)
