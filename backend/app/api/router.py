from fastapi import APIRouter

from app.api.routes import dashboard, ml, pipeline


api_router = APIRouter()
api_router.include_router(dashboard.router)
api_router.include_router(ml.router)
api_router.include_router(pipeline.router)
