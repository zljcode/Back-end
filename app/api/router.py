from fastapi import APIRouter

from app.api.routes.health import router as health_router
from app.api.routes.visitor import router as visitor_router

api_router = APIRouter()
api_router.include_router(health_router, tags=["health"])
api_router.include_router(visitor_router,tags=["visitor"])
