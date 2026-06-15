import __main__
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router

# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

app = FastAPI(
    title="Visitor Risk Demo API",
    version="0.1.0",
)

# 开启跨域访问  前端访问后端
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


# if __name__ == __main__:
    
    
