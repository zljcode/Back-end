# Demo Back-end

这是一个用于访客风险展示 Demo 的 FastAPI 后端。前端 GeeGuard SDK 产出
`gee_token` 后，会调用本项目的 `POST /api/visitor` 接口；后端再继续请求
g2-service 的 `GeeTokenQuery`，把匿名模式、VPN、IP 类型、风险等级、风险码、
指纹信息整合后返回给前端页面。

## 项目结构

- `app/main.py`：FastAPI 应用入口
- `app/api/routes/health.py`：健康检查接口
- `app/service/gee_token_query_service.py`：GeeTokenQuery 调用封装与签名生成
- `requirements.txt`：Python 依赖列表

## G2 Service 配置

先根据 `.env.example` 创建本地 `.env`，或者直接在 shell 中导出环境变量。
真实凭证不要提交到 git。

```bash
export G2_GEE_TOKEN_QUERY_URL=http://127.0.0.1:9999/g5/api/v1/token_query
export G2_APP_ID=your_app_id
export G2_PRIVATE_KEY=your_private_key
```

`G2_PRIVATE_KEY` 必须保留在本地环境中，不能写入仓库。前端 GeeGuard SDK 使用的
`appId` 属于公开标识，它不能替代后端私钥。

当前链路中，前端 GeeGuard SDK 会先完成 `pre_load -> client_report`，然后把返回
的 `gee_token` 传给本后端。如果请求里没有 `gee_token`，后端会回退到本地 mock
数据，保证页面仍然可展示。

`token_query` 请求体示例：

```json
{
  "app_id": "your_app_id",
  "sign_token": "...",
  "gen_time": 1710000000,
  "gee_token": "...",
  "scene": "activity",
  "attr": {
    "user_ip": "203.0.113.10",
    "op_timestamp": 1710000000
  }
}
```

## 启动方式

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

请求示例：

```bash
curl -X POST 'http://127.0.0.1:8000/api/visitor' \
  -H 'content-type: application/json' \
  -H 'x-forwarded-for: 203.0.113.10' \
  -d '{
    "gee_token": "replace-with-sdk-returned-geetoken",
    "scene": "activity",
    "environment": {
      "browser_name": "Chrome",
      "device_type": "Desktop"
    }
  }'
```
