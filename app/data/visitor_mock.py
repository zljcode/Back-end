from app.schemas.visitor import ScenarioType


DEFAULT_SCENARIO:ScenarioType = "pass"

# 基础 mock 
BASIC_MOCK = {
        "visitor_id": "GEE3-01-a8f4c2e9b170",
        "risk_level": "pass",
        "risk_code": [],
        "risk_summary": "Trusted",
        "network": {
            "ip": "127.0.0.1",
            "ip_type": None,
            "is_vpn": None,
            "vpn_confidence": "unknown",
        }
}

# 全部mock
VISITOR_MOCK = {
    "pass": {
        "visitor_id": "GEE3-01-a8f4c2e9b170",
        "risk_level": "pass",
        "risk_code": [],
        "risk_summary": "Trusted",
        "network": {
            "ip": "127.0.0.1",
            "ip_type": None,
            "is_vpn": None,
            "vpn_confidence": "unknown",
        },
        "environment": {
            "browser_name": "Chrome",
            "browser_version": "136.0.0.0",
            "os_name": "Windows",
            "device_type": "Desktop",
            "is_incognito": None,
            "incognito_confidence": "unknown",
            "language": "zh-CN",
            "timezone": "Asia/Shanghai",
            "platform": "Win32",
            "screen_resolution": "1920x1080",
            "hardware_concurrency": 8,
            "device_memory": 8,
        },
        "signals": {
            "user_agent": "mock-user-agent",
            "canvas_fingerprint": None,
            "webgl_vendor": None,
            "webgl_renderer": None,
        },
        "meta": {
            "request_time": "2026-06-12T00:00:00+08:00",
        },
    },
    
    
    "review": {
        "visitor_id": "GEE3-01-a8f4c2e9b170",
        "risk_level": "review",
        "risk_code": [],
        "risk_summary": "Trusted",
        "network": {
            "ip": "127.0.0.1",
            "ip_type": None,
            "is_vpn": None,
            "vpn_confidence": "unknown",
        },
        "environment": {
            "browser_name": "Chrome",
            "browser_version": "136.0.0.0",
            "os_name": "Windows",
            "device_type": "Desktop",
            "is_incognito": None,
            "incognito_confidence": "unknown",
            "language": "zh-CN",
            "timezone": "Asia/Shanghai",
            "platform": "Win32",
            "screen_resolution": "1920x1080",
            "hardware_concurrency": 8,
            "device_memory": 8,
        },
        "signals": {
            "user_agent": "mock-user-agent",
            "canvas_fingerprint": None,
            "webgl_vendor": None,
            "webgl_renderer": None,
        },
        "meta": {
            "request_time": "2026-06-12T00:00:00+08:00",
        },
    },
    
    
    "reject": {        
        "visitor_id": "GEE3-01-a8f4c2e9b170",
        "risk_level": "reject",
        "risk_code": [],
        "risk_summary": "Trusted",
        "network": {
            "ip": "127.0.0.1",
            "ip_type": None,
            "is_vpn": None,
            "vpn_confidence": "unknown",
        },
        "environment": {
            "browser_name": "Chrome",
            "browser_version": "136.0.0.0",
            "os_name": "Windows",
            "device_type": "Desktop",
            "is_incognito": None,
            "incognito_confidence": "unknown",
            "language": "zh-CN",
            "timezone": "Asia/Shanghai",
            "platform": "Win32",
            "screen_resolution": "1920x1080",
            "hardware_concurrency": 8,
            "device_memory": 8,
        },
        "signals": {
            "user_agent": "mock-user-agent",
            "canvas_fingerprint": None,
            "webgl_vendor": None,
            "webgl_renderer": None,
        },
        "meta": {
            "request_time": "2026-06-12T00:00:00+08:00",
        },
        },
}
