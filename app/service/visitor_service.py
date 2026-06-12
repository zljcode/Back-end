from copy import deepcopy
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

    # 这里采用深拷贝的目的是为了不把全局mock数据改掉,后续请求会串数据
    profile_data = _merge_request_into_profile(payload, profile)

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


# 私有检查逻辑函数
def _merge_request_into_profile(payload: VisitorRequest, profile: dict) -> dict:

    # 这里采用深拷贝的目的是为了不把全局mock数据改掉,后续请求会串数据
    profile_data = deepcopy(profile)

    if payload.environment and payload.environment.browser_name is not None:
        profile_data["environment"]["browser_name"] = payload.environment.browser_name
    if payload.environment and payload.environment.browser_version is not None:
        profile_data["environment"]["browser_version"] = payload.environment.browser_version
    if payload.environment and payload.environment.os_name is not None:
        profile_data["environment"]["os_name"] = payload.environment.os_name
    if payload.environment and payload.environment.device_type is not None:
        profile_data["environment"]["device_type"] = payload.environment.device_type
    if payload.signals and payload.signals.user_agent is not None:
        profile_data["signals"]["user_agent"] = payload.signals.user_agent
    if payload.signals and payload.signals.canvas_fingerprint is not None:
        profile_data["signals"]["canvas_fingerprint"] = payload.signals.canvas_fingerprint
    if payload.signals and payload.signals.webgl_vendor is not None:
        profile_data["signals"]["webgl_vendor"] = payload.signals.webgl_vendor
    if payload.signals and payload.signals.webgl_renderer is not None:
        profile_data["signals"]["webgl_renderer"] = payload.signals.webgl_renderer
    if payload.environment and payload.environment.language is not None:
        profile_data["environment"]["language"] = payload.environment.language
    if payload.environment and payload.environment.timezone is not None:
        profile_data["environment"]["timezone"] = payload.environment.timezone
    if payload.environment and payload.environment.platform is not None:
        profile_data["environment"]["platform"] = payload.environment.platform
    if payload.environment and payload.environment.screen_resolution is not None:
        profile_data["environment"][
            "screen_resolution"
        ] = payload.environment.screen_resolution
    if payload.environment and payload.environment.hardware_concurrency is not None:
        profile_data["environment"][
            "hardware_concurrency"
        ] = payload.environment.hardware_concurrency
    if payload.environment and payload.environment.device_memory is not None:
        profile_data["environment"]["device_memory"] = payload.environment.device_memory

    return profile_data
