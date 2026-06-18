import os

# 调用 g2-service 的 GeeTokenQuery 服务
G2_GEE_TOKEN_QUERY_URL = os.getenv(
    "G2_GEE_TOKEN_QUERY_URL",
    "http://127.0.0.1:9999/g5/api/v1/token_query",
)
G2_APP_ID = os.getenv("G2_APP_ID")
G2_PRIVATE_KEY = os.getenv("G2_PRIVATE_KEY")
