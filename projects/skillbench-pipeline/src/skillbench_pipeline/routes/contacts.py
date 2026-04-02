"""Contact routes."""

from fastapi import APIRouter

from skillbench_pipeline.config import Settings
from skillbench_pipeline.db import create_contact, list_contacts, update_contact
from skillbench_pipeline.models import ContactCreate, ContactUpdate

router = APIRouter(tags=["contacts"])


def _db() -> str:
    return str(Settings().db_abs_path)


@router.get("/contacts")
async def api_list_contacts(org_id: int | None = None):
    return await list_contacts(_db(), org_id=org_id)


@router.post("/contacts")
async def api_create_contact(body: ContactCreate):
    contact_id = await create_contact(_db(), **body.model_dump(exclude_none=True))
    return {"id": contact_id}


@router.put("/contacts/{contact_id}")
async def api_update_contact(contact_id: int, body: ContactUpdate):
    await update_contact(_db(), contact_id, **body.model_dump(exclude_none=True))
    return {"ok": True}
