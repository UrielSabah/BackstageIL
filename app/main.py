from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import api_router
from fastapi.responses import ORJSONResponse, FileResponse
from pathlib import Path


app = FastAPI(
    title="BackstageIL API",
    description="API for technical information for backstage's",
    version="1.0.0",
    default_response_class=ORJSONResponse
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins, replace '*' with specific URLs if needed
    allow_credentials=True,
    allow_methods=["GET"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

app.include_router(api_router)

@app.get("/ads.txt", include_in_schema=False)
async def ads():
    return FileResponse(Path("static/ads.txt"))
