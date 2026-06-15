from copy import deepcopy
from datetime import datetime, timezone, timedelta

from fastapi import HTTPException

from app.data.visitor_mock import DEFAULT_SCENARIO, VISITOR_MOCK
from app.schemas.visitor import ScenarioType, VisitorRequest, VisitorResponse


def get_visitor_profile(scenario: ScenarioType = DEFAULT_SCENARIO) -> VisitorResponse:
    profile = _get_profile_or_raise(scenario)
    return VisitorResponse(**profile)


def create_visitor_profile(
    payload: VisitorRequest, scenario: ScenarioType = DEFAULT_SCENARIO
) -> VisitorResponse:
    profile = _get_profile_or_raise(scenario)
    profile_data = deepcopy(profile)

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
        "is_incognito": None,
        "incognito_confidence": "unknown",
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
