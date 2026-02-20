"""
Neon (PostgreSQL) async connection via SQLAlchemy + asyncpg.

You set DB_URL to your Neon connection string (e.g. with ?sslmode=require).
We have to adjust it because:
- SQLAlchemy async needs postgresql+asyncpg:// (not postgresql://).
- asyncpg does not accept sslmode in the URL; we strip it and pass ssl=True instead.
"""
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings


def _engine_url_and_ssl() -> tuple[str, dict]:
    """
    Build URL and connect_args for create_async_engine from DB_URL.
    - Switches postgresql:// → postgresql+asyncpg://.
    - Removes sslmode (and related) from the URL and sets connect_args["ssl"] = True
      when SSL is required (Neon uses sslmode=require; asyncpg expects ssl=True).
    """
    url = settings.DB_URL.strip()
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+asyncpg://", 1)
    parsed = urlparse(url)
    qs = parse_qs(parsed.query, keep_blank_values=True)
    ssl_keys = ("sslmode", "sslcert", "sslkey", "sslrootcert", "sslcrl")
    use_ssl = (
        qs.get("sslmode")
        and qs["sslmode"][0].lower() in ("require", "verify-full", "verify-ca", "prefer", "allow")
    )
    for k in ssl_keys:
        qs.pop(k, None)
    new_query = urlencode(qs, doseq=True)
    clean_url = urlunparse(parsed._replace(query=new_query))
    connect_args = {"ssl": True} if use_ssl else {}
    return clean_url, connect_args


async def init_db(app: FastAPI) -> None:
    """Create async engine and session factory; attach to app.state."""
    url, connect_args = _engine_url_and_ssl()
    engine = create_async_engine(
        url,
        connect_args=connect_args,
        pool_size=settings.DB_POOL_SIZE,
        max_overflow=settings.DB_MAX_OVERFLOW,
        pool_pre_ping=True,
        echo=False,
    )
    session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )
    app.state.async_engine = engine
    app.state.async_session_factory = session_factory


async def close_db(app: FastAPI) -> None:
    """Dispose engine on shutdown."""
    engine: AsyncEngine | None = getattr(app.state, "async_engine", None)
    if engine is not None:
        await engine.dispose()
        app.state.async_engine = None
