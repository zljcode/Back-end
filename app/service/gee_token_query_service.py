import hmac
import time
from typing import Optional

import httpx

from app.core.setting import G2_APP_ID, G2_GEE_TOKEN_QUERY_URL, G2_PRIVATE_KEY

# 建立登录token，用于token_query接口的调用方身份校验
def build_sign_token(app_id: str, gen_time: int, private_key: str) -> str:
    msg = f"{app_id}{gen_time}"
    return hmac.new(
        private_key.encode(),
        msg.encode(),
        digestmod="SHA256",
    ).hexdigest()

# 建立 geetoken查询负载
def build_geetoken_query_payload(
    gee_token: str,
    user_ip: str,
    sign_token: str,
    gen_time: int,
    scene: Optional[str] = None,
) -> dict:
    payload = {
        "app_id": G2_APP_ID,
        "sign_token": sign_token,
        "gen_time": gen_time,
        "gee_token": gee_token,
        "attr": {
            "user_ip": user_ip,
            "op_timestamp": int(time.time()),
        },
    }

    if scene:
        payload["scene"] = scene

    return payload


def prepare_geetoken_query_request(
    gee_token: str,
    user_ip: str,
    private_key: str,
    scene: Optional[str] = None,
) -> dict:
    gen_time = int(time.time())
    sign_token = build_sign_token(G2_APP_ID, gen_time, private_key)
    payload = build_geetoken_query_payload(
        gee_token=gee_token,
        user_ip=user_ip,
        sign_token=sign_token,
        gen_time=gen_time,
        scene=scene,
    )

    return {
        "gen_time": gen_time,
        "sign_token": sign_token,
        "payload": payload,
    }

# 调用g2_service 的 gee_token_query接口
def query_geetoken(gee_token: str, user_ip: str, scene: Optional[str] = None) -> dict:
    if not G2_APP_ID or not G2_PRIVATE_KEY:
        raise ValueError("G2_APP_ID or G2_PRIVATE_KEY is not configured")
    if not gee_token:
        raise ValueError("gee_token is required")

    request_data = prepare_geetoken_query_request(
        gee_token=gee_token,
        user_ip=user_ip,
        private_key=G2_PRIVATE_KEY,
        scene=scene,
    )
    # 建立好请求参数后访问 g2_service 中的gee_token_query获取风险评估结果
    try:
        response = httpx.post(
            G2_GEE_TOKEN_QUERY_URL,
            json=request_data["payload"],
            timeout=5.0,
        )
        response.raise_for_status()
    except httpx.HTTPError as exc:
        raise RuntimeError(f"geetoken query request failed: {exc}") from exc

    return response.json()
