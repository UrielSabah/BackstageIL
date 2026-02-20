from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, FileResponse, JSONResponse

from app.routes import api_router
from app.db.neondb import init_db, close_db
from app.core.exceptions import DomainException, handle_domain_exception, handle_db_exception

BASE_DIR = Path(__file__).resolve().parent.parent


def _response_content(detail: dict | str) -> dict:
    """Normalize exception detail for JSON response."""
    return detail if isinstance(detail, dict) else {"detail": detail}


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await init_db(fastapi_app)
    yield
    await close_db(fastapi_app)


app = FastAPI(
    title="BackstageIL API",
    description="API for technical information for backstage venues and music halls",
    version="1.0.0",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.exception_handler(DomainException)
async def domain_exception_handler(_request: Request, exc: DomainException) -> JSONResponse:
    http_exc = handle_domain_exception(exc)
    return JSONResponse(status_code=http_exc.status_code, content=_response_content(http_exc.detail))


@app.exception_handler(Exception)
async def unhandled_exception_handler(_request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, HTTPException):
        return JSONResponse(status_code=exc.status_code, content=_response_content(exc.detail))
    http_exc = handle_db_exception(exc)
    return JSONResponse(status_code=http_exc.status_code, content=_response_content(http_exc.detail))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Replace '*' with allowed origins in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/ads.txt", include_in_schema=False)
async def ads():
    return FileResponse(BASE_DIR / "static" / "ads.txt")
