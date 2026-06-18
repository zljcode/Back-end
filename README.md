# Demo Back-end

FastAPI backend scaffold for the visitor-risk demo. The POST visitor API
receives the `gee_token` produced by the front-end GeeGuard SDK and calls
g2-service `GeeTokenQuery` to expose anonymous mode, VPN, IP type, risk level,
risk code, and fingerprint ids.

## Structure

- `app/main.py`: FastAPI application entry
- `app/api/routes/health.py`: basic health route
- `app/service/gee_token_query_service.py`: signed GeeTokenQuery client
- `requirements.txt`: Python dependencies

## G2 Service

Create a local `.env` from `.env.example`, or export the variables in your shell.
Do not commit real credentials.

```bash
export G2_GEE_TOKEN_QUERY_URL=http://127.0.0.1:9999/g5/api/v1/token_query
export G2_APP_ID=your_app_id
export G2_PRIVATE_KEY=your_private_key
```

`G2_PRIVATE_KEY` must stay out of git. The browser-side GeeGuard `appId` used by
the front-end SDK is a public identifier, not a replacement for the private
key.

The front-end GeeGuard SDK handles `pre_load -> client_report` and passes the
returned `gee_token` to this backend. When no token is supplied, the backend
returns local mock data.

`token_query` payload:

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

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Example:

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
