from typing import Union
from pydantic import BaseModel
from typing_extensions import Literal

ScenarioType = Literal["pass","review","reject"]


class Network(BaseModel):
    ip: str
    ip_type: str | None
    is_vpn: bool | None
    vpn_confidence: Literal["detected", "not_detected", "unknown"]


class Environment(BaseModel):
    browser_name: str  # 浏览器名称，如 Chrome、Edge、Firefox
    browser_version: str  # 浏览器版本号，如 149.0.0.0
    os_name: str  # 操作系统，如 Windows、macOS、Linux
    device_type: Literal[
        "Desktop", "Mobile", "Tablet"
    ]  # 设备类型，如 Desktop、Mobile、Tablet
    is_incognito: bool | None  # 是否无痕/隐身模式，无法确定时为 None
    incognito_confidence: Literal[
        "detected", "not_detected", "unknown"
    ]  # 无痕模式判断的置信度，如 high、low
    language: str  # 浏览器语言，如 zh-CN、en-US
    timezone: str  # 时区，如 Asia/Shanghai
    platform: str  # 平台标识，如 Win32、Linux x86_64
    screen_resolution: str  # 屏幕分辨率，如 1920x1080
    hardware_concurrency: int | str  # CPU 逻辑核心数，获取失败时为字符串
    device_memory: int | str  # 设备内存（GB），获取失败时为字符串


class Signals(BaseModel):
    user_agent: str
    canvas_fingerprint: str | None
    webgl_vendor: str | None
    webgl_renderer: str | None


class Meta(BaseModel):
    request_time: str


class VisitorResponse(BaseModel):
    visitor_id: str
    risk_level: ScenarioType
    risk_code: list[str]
    risk_summary: str
    network: Network
    environment: Environment
    signals: Signals
    meta: Meta


# 将请求字段进行分层,访问环境
class VisitorEnvironmentInput(BaseModel):
    browser_name: str | None = None
    browser_version: str | None = None
    os_name: str | None = None
    device_type: str | None = None
    language: str | None = None
    timezone: str | None = None
    platform: str | None = None
    screen_resolution: str | None = None
    hardware_concurrency: Union[int, str] | None = None
    device_memory: Union[int, str] | None = None


# 访问标志输入
class VisitorSignalsInput(BaseModel):
    user_agent: str | None = None
    canvas_fingerprint: str | None = None
    webgl_vendor: str | None = None
    webgl_renderer: str | None = None


# 请求模型 前端收集的数据
class VisitorRequest(BaseModel):
    environment: VisitorEnvironmentInput | None = None
    signals: VisitorSignalsInput | None = None
