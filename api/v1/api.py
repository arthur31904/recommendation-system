from fastapi import APIRouter
from .recommendation import recommendation_views

api_router = APIRouter()


api_router.include_router(recommendation_views.router, prefix="/recommendation_api", tags=["recommendation_api"])
