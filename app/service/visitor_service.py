from copy import deepcopy
from datetime import datetime, timezone, timedelta
import ipaddress

from fastapi import HTTPException

from app.data.visitor_mock import DEFAULT_SCENARIO, VISITOR_MOCK
from app.schemas.visitor import ScenarioType, VisitorRequest, VisitorResponse


def get_visitor_profile(scenario: ScenarioType = DEFAULT_SCENARIO) -> VisitorResponse:
    profile = _get_profile_or_raise(scenario)
    return VisitorResponse(**profile)

# 建立访客信息
def create_visitor_profile(
    payload: VisitorRequest, scenario: ScenarioType = DEFAULT_SCENARIO,client_ip :str ="unknown"
) -> VisitorResponse:
    profile = _get_profile_or_raise(scenario)
    profile_data = deepcopy(profile)

    profile_data["network"] = _build_network_from_ip(client_ip,profile)
    profile_data["environment"] = _build_environment_from_payload(payload)
    profile_data["signals"] = _build_signals_from_payload(payload)
    profile_data["meta"] = {
        "request_time": _current_request_time(),
    }

    return VisitorResponse(**profile_data)


# 私有判定函数
def _get_profile_or_raise(scenario: ScenarioType) -> dict:
    profile = VISITOR_MOCK.get(scenario)

    if profile is None:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "invalid_scenario",
                "message": f"invalid scenario :{scenario}",
            },
        )

    return profile


def _build_environment_from_payload(payload: VisitorRequest) -> dict:
    environment = payload.environment

    return {
        "browser_name": environment.browser_name if environment else "unknown",
        "browser_version": environment.browser_version if environment else "unknown",
        "os_name": environment.os_name if environment else "unknown",
        "device_type": environment.device_type if environment else "Desktop",
        "is_incognito": environment.is_incognito if environment else None,
        "incognito_confidence": (
    environment.incognito_confidence if environment and environment.incognito_confidence else "unknown"
),
        "language": environment.language if environment else "unknown",
        "timezone": environment.timezone if environment else "unknown",
        "platform": environment.platform if environment else "unknown",
        "screen_resolution": environment.screen_resolution if environment else "unknown",
        "hardware_concurrency": environment.hardware_concurrency if environment else "unknown",
        "device_memory": environment.device_memory if environment else "unknown",
    }


def _build_signals_from_payload(payload: VisitorRequest) -> dict:
    signals = payload.signals

    return {
        "user_agent": signals.user_agent if signals else "unknown",
        "canvas_fingerprint": signals.canvas_fingerprint if signals else None,
        "webgl_vendor": signals.webgl_vendor if signals else None,
        "webgl_renderer": signals.webgl_renderer if signals else None,
    }


def _current_request_time() -> str:
    shanghai_tz = timezone(timedelta(hours=8))
    return datetime.now(shanghai_tz).isoformat()

# 拿到真实ip进行返回
def _build_network_from_ip(client_ip:str,profile :dict) -> dict: 
    network = deepcopy(profile["network"])
    
    vpn_result = _detect_vpn(client_ip)
    
    network["ip"] = client_ip
    network["is_vpn"] = None
    network["vpn_confidence"] = "unknown"
    network["ip_type"] = vpn_result["ip_type"]
    return network

#  这里后续接入真实可用的找到vpn的东西
def _detect_vpn(client_ip: str) -> dict:
    if client_ip in {"127.0.0.1", "::1", "unknown"}:
        return {
            "is_vpn": None,
            "vpn_confidence": "unknown",
            "ip_type": None,
        }
        
    
    try:
        ip_obj = ipaddress.ip_address(client_ip)
    except ValueError:
     return {
        "is_vpn": None,
        "vpn_confidence": "unknown",
        "ip_type": None,
    }
    # 本机回环地址 私网地址,保留地址,非法IP字符串
    if ip_obj.is_private or ip_obj.is_loopback or ip_obj.is_reserved or ip_obj.is_link_local:
        return {
        "is_vpn": None,
        "vpn_confidence": "unknown",
        "ip_type": None,
    }
   
    return {
        "is_vpn": None,
        "vpn_confidence": "unknown",
        "ip_type": None,
    }            


