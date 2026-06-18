from typing import List, Optional, Union
from pydantic import BaseModel
from typing_extensions import Literal

ScenarioType = Literal["pass", "review", "reject"]


class Network(BaseModel):
    ip: str
    ip_type: Optional[Union[int, str]]
    is_vpn: Optional[bool]
    vpn_confidence: Literal["detected", "not_detected", "unknown"]


class Environment(BaseModel):
    browser_name: str  # 浏览器名称，如 Chrome、Edge、Firefox
    browser_version: str  # 浏览器版本号，如 149.0.0.0
    os_name: str  # 操作系统，如 Windows、macOS、Linux
    device_type: Literal[
        "Desktop", "Mobile", "Tablet"
    ]  # 设备类型，如 Desktop、Mobile、Tablet
    is_incognito: Optional[bool]  # 是否无痕/隐身模式，无法确定时为 None
    incognito_confidence: Literal[
        "detected", "not_detected", "unknown"
    ]  # 无痕模式判断的置信度，如 high、low
    language: str  # 浏览器语言，如 zh-CN、en-US
    timezone: str  # 时区，如 Asia/Shanghai
    platform: str  # 平台标识，如 Win32、Linux x86_64
    screen_resolution: str  # 屏幕分辨率，如 1920x1080
    hardware_concurrency: Union[int, str]  # CPU 逻辑核心数，获取失败时为字符串
    device_memory: Union[int, str]  # 设备内存（GB），获取失败时为字符串


class Signals(BaseModel):
    user_agent: str  # 浏览器标识符
    canvas_fingerprint: Optional[
        str
    ]  # 在让浏览器在 Canvas 上绘制图形，不同设备/驱动渲染结果有细微差异，对结果做哈希得到的指纹值。
    webgl_vendor: Optional[str]  # GPU厂商的名称,
    webgl_renderer: Optional[str]  # GPU具体型号


class Meta(BaseModel):
    request_time: str
    client_report_used: bool = False
    client_report_status: str = "skipped"
    geetoken_query_used: bool = False
    geetoken_query_status: str = "skipped"
    token_source: str = "none"


class Fingerprint(BaseModel):
    local_id: Optional[str] = None
    root_id: Optional[str] = None
    sign: Optional[str] = None
    server_ts: Optional[int] = None
    client_ts: Optional[int] = None


class VisitorResponse(BaseModel):
    visitor_id: str
    risk_level: ScenarioType
    risk_code: List[Union[int, str]]
    risk_summary: str
    network: Network
    environment: Environment
    signals: Signals
    fingerprint: Optional[Fingerprint] = None
    meta: Meta


# 将请求字段进行分层,访问环境
class VisitorEnvironmentInput(BaseModel):
    browser_name: Optional[str] = None
    browser_version: Optional[str] = None
    os_name: Optional[str] = None
    device_type: Optional[str] = None
    language: Optional[str] = None
    timezone: Optional[str] = None
    platform: Optional[str] = None
    screen_resolution: Optional[str] = None
    hardware_concurrency: Optional[Union[int, str]] = None
    device_memory: Optional[Union[int, str]] = None
    is_incognito: Optional[bool] = None
    incognito_confidence: Optional[str] = None


# 访问标志输入
class VisitorSignalsInput(BaseModel):
    user_agent: Optional[str] = None
    canvas_fingerprint: Optional[str] = None
    webgl_vendor: Optional[str] = None
    webgl_renderer: Optional[str] = None


# 请求模型 前端收集的数据
class VisitorRequest(BaseModel):
    gee_token: Optional[str] = None
    scene: Optional[str] = None
    environment: Optional[VisitorEnvironmentInput] = None
    signals: Optional[VisitorSignalsInput] = None
