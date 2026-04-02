"""Dashboard aggregation routes."""

from fastapi import APIRouter

from skillbench_pipeline.config import Settings
from skillbench_pipeline.db import list_activities, pipeline_summary, pipeline_velocity

router = APIRouter(tags=["dashboard"])


def _db() -> str:
    return str(Settings().db_abs_path)


@router.get("/dashboard/summary")
async def api_summary():
    return await pipeline_summary(_db())


@router.get("/dashboard/velocity")
async def api_velocity():
    return await pipeline_velocity(_db())


@router.get("/dashboard/feed")
async def api_feed(days: int = 7, limit: int = 20):
    return await list_activities(_db(), days=days, limit=limit)
