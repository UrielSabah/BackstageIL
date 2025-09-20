from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse, FileResponse
from pathlib import Path
from contextlib import asynccontextmanager

from app.routes import api_router
from app.db.neondb import init_db_pool, close_db_pool
from app.db.awsdb import init_aws,close_aws


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await init_db_pool(fastapi_app)
    await init_aws()

    yield

    await close_aws()
    await close_db_pool(fastapi_app)


app = FastAPI(
    title="BackstageIL API",
    description="API for technical information for backstage's",
    version="1.0.0",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #todo: Replace '*' with allowed origins in prod
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/ads.txt", include_in_schema=False)
async def ads():
    return FileResponse(Path("static/ads.txt"))
