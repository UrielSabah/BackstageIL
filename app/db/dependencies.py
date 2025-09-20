from fastapi import Request
import asyncpg

async def get_db_pool(request: Request) -> asyncpg.Pool:
    return request.app.state.db_pool

