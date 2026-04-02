"""FastAPI app for SkillBench Pipeline dashboard."""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from skillbench_pipeline.config import Settings
from skillbench_pipeline.routes import orgs, contacts, opportunities, activities, reminders, dashboard

STATIC_DIR = Path(__file__).resolve().parent.parent.parent / "static"

app = FastAPI(title="SkillBench Pipeline", version="0.1.0")

# Auth middleware
@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    settings = Settings()
    if settings.auth_token:
        # Check header or query param
        auth = request.headers.get("Authorization", "")
        token_param = request.query_params.get("token", "")
        expected = f"Bearer {settings.auth_token}"
        if auth != expected and token_param != settings.auth_token:
            # Allow static files and root without auth
            if request.url.path.startswith("/api/"):
                from fastapi.responses import JSONResponse
                return JSONResponse({"error": "Unauthorized"}, status_code=401)
    return await call_next(request)


# Startup: init DB
@app.on_event("startup")
async def startup():
    from skillbench_pipeline.db import init_db
    settings = Settings()
    await init_db(str(settings.db_abs_path))


# API routes
app.include_router(orgs.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")
app.include_router(opportunities.router, prefix="/api")
app.include_router(activities.router, prefix="/api")
app.include_router(reminders.router, prefix="/api")
app.include_router(dashboard.router, prefix="/api")

# Static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def root():
    return FileResponse(str(STATIC_DIR / "index.html"))
