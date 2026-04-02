"""Opportunity routes."""

from fastapi import APIRouter, HTTPException

from skillbench_pipeline.config import Settings
from skillbench_pipeline.db import (
    create_opportunity, delete_opportunity, get_opportunity, list_opportunities,
    move_opportunity_stage, update_opportunity,
)
from skillbench_pipeline.models import OppCreate, OppUpdate, StageUpdate

router = APIRouter(tags=["opportunities"])


def _db() -> str:
    return str(Settings().db_abs_path)


@router.get("/opps")
async def api_list_opps(stage: str | None = None, org_id: int | None = None):
    return await list_opportunities(_db(), stage=stage, org_id=org_id)


@router.get("/opps/{opp_id}")
async def api_get_opp(opp_id: int):
    opp = await get_opportunity(_db(), opp_id)
    if not opp:
        raise HTTPException(404, "Opportunity not found")
    return opp


@router.post("/opps")
async def api_create_opp(body: OppCreate):
    opp_id = await create_opportunity(_db(), **body.model_dump(exclude_none=True))
    return {"id": opp_id}


@router.put("/opps/{opp_id}")
async def api_update_opp(opp_id: int, body: OppUpdate):
    await update_opportunity(_db(), opp_id, **body.model_dump(exclude_none=True))
    return {"ok": True}


@router.delete("/opps/{opp_id}")
async def api_delete_opp(opp_id: int):
    opp = await get_opportunity(_db(), opp_id)
    if not opp:
        raise HTTPException(404, "Opportunity not found")
    await delete_opportunity(_db(), opp_id)
    return {"ok": True}


@router.patch("/opps/{opp_id}/stage")
async def api_move_stage(opp_id: int, body: StageUpdate):
    try:
        await move_opportunity_stage(_db(), opp_id, body.stage.value)
    except ValueError as e:
        raise HTTPException(404, str(e))
    return {"ok": True}
