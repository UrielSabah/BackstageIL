from collections.abc import AsyncGenerator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

async def get_async_session(request: Request) -> AsyncGenerator[AsyncSession, None]:
    """Request-scoped async session: commit on success, rollback on error."""
    factory: async_sessionmaker[AsyncSession] = request.app.state.async_session_factory
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
