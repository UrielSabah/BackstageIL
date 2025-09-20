import asyncpg
from fastapi import HTTPException, status
from app.core.logger import setup_logger

logger = setup_logger(__name__)

def handle_db_exception(e: Exception) -> HTTPException:
    if isinstance(e, asyncpg.UniqueViolationError):
        return HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Duplicate entry")
    if isinstance(e, asyncpg.ForeignKeyViolationError):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid reference")
    if isinstance(e, asyncpg.PostgresError):
        logger.error("Database error: %s", str(e))
        return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database error")
    logger.exception("Unexpected error: %s", str(e))
    return HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")