"""Organization routes."""

from fastapi import APIRouter

from skillbench_pipeline.config import Settings
from skillbench_pipeline.db import create_org, get_org, list_orgs, update_org
from skillbench_pipeline.models import OrgCreate, OrgUpdate

router = APIRouter(tags=["organizations"])


def _db() -> str:
    return str(Settings().db_abs_path)


@router.get("/orgs")
async def api_list_orgs():
    return await list_orgs(_db())


@router.get("/orgs/{org_id}")
async def api_get_org(org_id: int):
    org = await get_org(_db(), org_id)
    if not org:
        from fastapi import HTTPException
        raise HTTPException(404, "Organization not found")
    return org


@router.post("/orgs")
async def api_create_org(body: OrgCreate):
    org_id = await create_org(_db(), **body.model_dump(exclude_none=True))
    return {"id": org_id}


@router.put("/orgs/{org_id}")
async def api_update_org(org_id: int, body: OrgUpdate):
    await update_org(_db(), org_id, **body.model_dump(exclude_none=True))
    return {"ok": True}
