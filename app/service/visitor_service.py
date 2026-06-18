from copy import deepcopy
from datetime import datetime, timezone, timedelta
import ipaddress
from typing import Optional

from fastapi import HTTPException

from app.data.visitor_mock import DEFAULT_SCENARIO, VISITOR_MOCK
from app.schemas.visitor import ScenarioType, VisitorRequest, VisitorResponse
from app.service.gee_token_query_service import query_geetoken


INCOGNITO_RISK_CODE = 20606 # 匿名/无痕模式访问 的风险码
VPN_RISK_CODE = 20500  # VPN异常的风险码
# 20400 普通无风险模式的风险码


def get_visitor_profile(scenario: ScenarioType = DEFAULT_SCENARIO) -> VisitorResponse:
    profile = _get_profile_or_raise(scenario)
    return VisitorResponse(**profile)


# 建立访客信息
def create_visitor_profile(
    payload: VisitorRequest,
    scenario: ScenarioType = DEFAULT_SCENARIO,
    client_ip: str = "unknown",
) -> VisitorResponse:
    profile = _get_profile_or_raise(scenario)
    profile_data = deepcopy(profile)
    # 结合gee_token_query的结果补充
    query_token = _resolve_query_token(payload)
    geetoken_result = _query_geetoken_if_available(
        query_token, client_ip, payload.scene
    )

    _apply_geetoken_query_result(profile_data, geetoken_result)
    profile_data["network"] = _build_network_from_ip(
        client_ip, profile, geetoken_result
    )
    profile_data["environment"] = _build_environment_from_payload(
        payload, geetoken_result
    )
    profile_data["signals"] = _build_signals_from_payload(payload)
    # 指纹信息
    profile_data["fingerprint"] = _build_fingerprint_from_geetoken_result(
        geetoken_result
    )
    profile_data["meta"] = {
        "request_time": _current_request_time(),
        "client_report_used": bool(query_token),
        "client_report_status": "success" if query_token else "skipped",
        "geetoken_query_used": bool(query_token),
        "geetoken_query_status": _build_geetoken_query_status(
            query_token, geetoken_result
        ),
        "token_source": _build_token_source(query_token),
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


def _build_environment_from_payload(
    payload: VisitorRequest, geetoken_result: Optional[dict] = None
) -> dict:
    environment = payload.environment
    incognito_result = _detect_incognito(payload, geetoken_result)

    return {
        "browser_name": _text_or_unknown(
            environment.browser_name if environment else None
        ),
        "browser_version": _text_or_unknown(
            environment.browser_version if environment else None
        ),
        "os_name": _text_or_unknown(environment.os_name if environment else None),
        "device_type": _normalize_device_type(
            environment.device_type if environment else None
        ),
        "is_incognito": incognito_result["is_incognito"],
        "incognito_confidence": incognito_result["incognito_confidence"],
        "language": _text_or_unknown(environment.language if environment else None),
        "timezone": _text_or_unknown(environment.timezone if environment else None),
        "platform": _text_or_unknown(environment.platform if environment else None),
        "screen_resolution": _text_or_unknown(
            environment.screen_resolution if environment else None
        ),
        "hardware_concurrency": _value_or_unknown(
            environment.hardware_concurrency if environment else None
        ),
        "device_memory": _value_or_unknown(
            environment.device_memory if environment else None
        ),
    }


def _build_signals_from_payload(payload: VisitorRequest) -> dict:
    signals = payload.signals

    return {
        "user_agent": _text_or_unknown(signals.user_agent if signals else None),
        "canvas_fingerprint": signals.canvas_fingerprint if signals else None,
        "webgl_vendor": signals.webgl_vendor if signals else None,
        "webgl_renderer": signals.webgl_renderer if signals else None,
    }


def _current_request_time() -> str:
    shanghai_tz = timezone(timedelta(hours=8))
    return datetime.now(shanghai_tz).isoformat()


# 组装网络维度信息，基础IP来自当前请求，VPN和ip_type优先使用token_query的放回结果
def _build_network_from_ip(
    client_ip: str, profile: dict, geetoken_result: Optional[dict] = None
) -> dict:
    network = deepcopy(profile["network"])

    vpn_result = _detect_vpn(client_ip, geetoken_result)

    network["ip"] = client_ip
    network["is_vpn"] = vpn_result["is_vpn"]
    network["vpn_confidence"] = vpn_result["vpn_confidence"]
    network["ip_type"] = vpn_result["ip_type"]
    return network


# 借鉴 g2-service 的 GeeTokenQuery：优先使用 env_check.is_vpn，其次使用 VPN 风险码 20500。
def _detect_vpn(client_ip: str, geetoken_result: Optional[dict] = None) -> dict:
    if geetoken_result and geetoken_result.get("status") != "error":
        data = _extract_geetoken_data(geetoken_result)
        env_check = data.get("env_check", {})
        risk_code = _normalize_risk_code(data.get("risk_code", []))
        is_vpn = env_check.get("is_vpn")

        if isinstance(is_vpn, bool):
            return {
                "is_vpn": is_vpn,
                "vpn_confidence": "detected" if is_vpn else "not_detected",
                "ip_type": data.get("ip_type"),
            }

        is_vpn = VPN_RISK_CODE in risk_code
        return {
            "is_vpn": is_vpn,
            "vpn_confidence": "detected" if is_vpn else "not_detected",
            "ip_type": data.get("ip_type"),
        }

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
    if (
        ip_obj.is_private
        or ip_obj.is_loopback
        or ip_obj.is_reserved
        or ip_obj.is_link_local
    ):
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


# 获取前端 GeeGuard SDK 返回的 gee_token
def _resolve_query_token(payload: VisitorRequest) -> Optional[str]:
    gee_token = payload.gee_token
    if isinstance(gee_token, str):
        gee_token = gee_token.strip()
    return gee_token or None


# 获取 gee_token_query 结果 只在请求中携带 gee_token 时才调用g2_service的 token_query
def _query_geetoken_if_available(
    query_token: Optional[str], client_ip: str, scene: Optional[str] = None
) -> Optional[dict]:
    if not query_token:
        return None

    try:
        return query_geetoken(query_token, client_ip, scene)
    except Exception as exc:
        return {
            "status": "error",
            "error": str(exc),
            "data": {},
        }

# 将g2_service返回的风险结果映射到demo响应结构
def _apply_geetoken_query_result(
    profile_data: dict, geetoken_result: Optional[dict]
) -> None:
    if not geetoken_result or geetoken_result.get("status") == "error":
        return
    # 同步风险水平、风险码和风险摘要
    risk_data = _extract_geetoken_data(geetoken_result)
    risk_level = risk_data.get("risk_level")
    risk_code = risk_data.get("risk_code")

    if risk_level in {"pass", "review", "reject"}:
        profile_data["risk_level"] = risk_level
        profile_data["risk_summary"] = _build_risk_summary(risk_level)

    if isinstance(risk_code, list):
        profile_data["risk_code"] = _normalize_risk_code(risk_code)

# 匿名模式优先读取env_check.is_incognito
def _detect_incognito(
    payload: VisitorRequest, geetoken_result: Optional[dict] = None
) -> dict:
    if geetoken_result and geetoken_result.get("status") != "error":
        data = _extract_geetoken_data(geetoken_result)
        env_check = data.get("env_check", {})
        risk_code = _normalize_risk_code(data.get("risk_code", []))
        is_incognito = env_check.get("is_incognito")

        if isinstance(is_incognito, bool):
            return {
                "is_incognito": is_incognito,
                "incognito_confidence": "detected" if is_incognito else "not_detected",
            }

        is_incognito = INCOGNITO_RISK_CODE in risk_code
        return {
            "is_incognito": is_incognito,
            "incognito_confidence": "detected" if is_incognito else "not_detected",
        }

    environment = payload.environment
    if environment and environment.is_incognito is not None:
        return {
            "is_incognito": environment.is_incognito,
            "incognito_confidence": _normalize_confidence(
                environment.incognito_confidence
            ),
        }

    return {
        "is_incognito": None,
        "incognito_confidence": "unknown",
    }


def _extract_geetoken_data(geetoken_result: dict) -> dict:
    data = geetoken_result.get("data", {})
    return data if isinstance(data, dict) else {}


def _normalize_risk_code(risk_code: object) -> list:
    if not isinstance(risk_code, list):
        return []

    normalized = []
    for code in risk_code:
        try:
            normalized.append(int(code))
        except (TypeError, ValueError):
            normalized.append(code)
    return normalized


def _normalize_confidence(confidence: Optional[str]) -> str:
    if confidence in {"detected", "not_detected", "unknown"}:
        return confidence
    return "unknown"


def _normalize_device_type(device_type: Optional[str]) -> str:
    if device_type in {"Desktop", "Mobile", "Tablet"}:
        return device_type
    return "Desktop"


def _text_or_unknown(value: Optional[str]) -> str:
    return value if value else "unknown"


def _value_or_unknown(value: object) -> object:
    return value if value is not None else "unknown"

# 建立指纹，从gee_token查询返回的结果中
def _build_fingerprint_from_geetoken_result(
    geetoken_result: Optional[dict],
) -> Optional[dict]:
    if not geetoken_result or geetoken_result.get("status") == "error":
        return None

    data = _extract_geetoken_data(geetoken_result)
    return {
        "local_id": data.get("local_id"),
        "root_id": data.get("root_id"),
        "sign": data.get("sign"),
        "server_ts": data.get("ts"),
        "client_ts": data.get("client_ts"),
    }

# 建立gee_token查询状态
def _build_geetoken_query_status(
    query_token: Optional[str], geetoken_result: Optional[dict]
) -> str:
    if not query_token:
        return "skipped"
    if not geetoken_result:
        return "failed"
    if geetoken_result.get("status") == "error":
        return "failed"
    return geetoken_result.get("status", "success")

# 标记当前风险结果使用的token来源 主要是前端 GeeGuard SDK 返回的 gee_token。
def _build_token_source(query_token: Optional[str]) -> str:
    if query_token:
        return "gee_token"
    return "none"


# 风险评估总结
def _build_risk_summary(risk_level: str) -> str:
    summary_map = {
        "pass": "Trusted",
        "review": "Needs Review",
        "reject": "High Risk",
    }
    return summary_map.get(risk_level, "Unknown")
