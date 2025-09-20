from fastapi import FastAPI
import asyncpg
from app.core.config import settings

DATABASE_URL = settings.DB_URL


async def init_db_pool(app: FastAPI):
    app.state.db_pool = await asyncpg.create_pool(
        dsn=DATABASE_URL,
        min_size=1,
        max_size=10,
        command_timeout=60,
    )

async def close_db_pool(app: FastAPI):
    await app.state.db_pool.close()