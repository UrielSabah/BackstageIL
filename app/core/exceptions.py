import asyncpg
from fastapi import HTTPException, status
from app.core.logger import setup_logger
from typing import Any
from enum import Enum

try:
    from sqlalchemy.exc import IntegrityError as SQLAlchemyIntegrityError
except ImportError:
    SQLAlchemyIntegrityError = None  # type: ignore[misc, assignment]

logger = setup_logger(__name__)


class ErrorCode(str, Enum):
    """Standard error codes for API responses"""
    MUSIC_HALL_NOT_FOUND = "MUSIC_HALL_NOT_FOUND"
    MUSIC_HALL_LIST_EMPTY = "MUSIC_HALL_LIST_EMPTY"
    NO_FIELDS_TO_UPDATE = "NO_FIELDS_TO_UPDATE"
    INVALID_UPDATE_FIELDS = "INVALID_UPDATE_FIELDS"
    DUPLICATE_ENTRY = "DUPLICATE_ENTRY"
    INVALID_REFERENCE = "INVALID_REFERENCE"
    DATABASE_ERROR = "DATABASE_ERROR"
    INTERNAL_ERROR = "INTERNAL_ERROR"


class ErrorType(str, Enum):
    """Error type categories"""
    NOT_FOUND = "NOT_FOUND"
    VALIDATION = "VALIDATION"
    CONFLICT = "CONFLICT"
    INTERNAL = "INTERNAL"


# Domain Exceptions (framework-agnostic)
# Using Strategy Pattern: Each exception knows how to convert itself to HTTP
class DomainException(Exception):
    """
    Base class for domain exceptions.
    
    Follows Strategy Pattern: Each exception implements to_http() method
    Follows Open/Closed Principle: New exceptions can be added without modifying handlers
    """
    
    def __init__(
        self,
        message: str,
        error_code: ErrorCode,
        error_type: ErrorType,
        status_code: int,
        details: dict[str, Any] | None = None
    ):
        """
        Initialize domain exception.
        
        Args:
            message: Human-readable error message
            error_code: Standard error code for API clients
            error_type: Category of error
            status_code: HTTP status code
            details: Additional error context/metadata
        """
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.error_type = error_type
        self.status_code = status_code
        self.details = details or {}
    
    def to_http(self) -> HTTPException:
        """
        Convert domain exception to HTTP exception.
        
        Strategy Pattern: Each exception knows how to convert itself.
        This allows polymorphism and follows Open/Closed Principle.
        """
        return HTTPException(
            status_code=self.status_code,
            detail={
                "error_code": self.error_code.value,
                "error_type": self.error_type.value,
                "message": self.message,
                **self.details
            }
        )


class MusicHallNotFoundError(DomainException):
    """Raised when a music hall is not found"""
    
    def __init__(self, hall_id: int):
        self.hall_id = hall_id
        super().__init__(
            message=f"Music hall with ID {hall_id} not found",
            error_code=ErrorCode.MUSIC_HALL_NOT_FOUND,
            error_type=ErrorType.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            details={"hall_id": hall_id}
        )


class MusicHallListEmptyError(DomainException):
    """Raised when no music halls are found in the database"""
    
    def __init__(self):
        super().__init__(
            message="No music halls found",
            error_code=ErrorCode.MUSIC_HALL_LIST_EMPTY,
            error_type=ErrorType.NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND
        )


class NoFieldsToUpdateError(DomainException):
    """Raised when update request contains no fields to update"""
    
    def __init__(self):
        super().__init__(
            message="No fields to update",
            error_code=ErrorCode.NO_FIELDS_TO_UPDATE,
            error_type=ErrorType.VALIDATION,
            status_code=status.HTTP_400_BAD_REQUEST
        )


class InvalidUpdateFieldsError(DomainException):
    """Raised when update request contains invalid field names"""
    
    def __init__(self, invalid_fields: set[str]):
        self.invalid_fields = list(invalid_fields)
        super().__init__(
            message=f"Invalid fields to update: {', '.join(invalid_fields)}",
            error_code=ErrorCode.INVALID_UPDATE_FIELDS,
            error_type=ErrorType.VALIDATION,
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"invalid_fields": self.invalid_fields}
        )


# HTTP Exception Handlers
# Using Strategy Pattern: Exceptions handle their own conversion
def handle_db_exception(e: Exception) -> HTTPException:
    """
    Convert database exceptions to HTTP exceptions.
    
    Handles asyncpg errors directly and SQLAlchemy IntegrityError
    (by delegating to the underlying asyncpg error when present).
    """
    # Unwrap SQLAlchemy IntegrityError to underlying asyncpg error when present
    if SQLAlchemyIntegrityError and isinstance(e, SQLAlchemyIntegrityError) and e.orig is not None:
        return handle_db_exception(e.orig)
    if isinstance(e, asyncpg.UniqueViolationError):
        return HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "error_code": ErrorCode.DUPLICATE_ENTRY.value,
                "error_type": ErrorType.CONFLICT.value,
                "message": "Duplicate entry"
            }
        )
    if isinstance(e, asyncpg.ForeignKeyViolationError):
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error_code": ErrorCode.INVALID_REFERENCE.value,
                "error_type": ErrorType.VALIDATION.value,
                "message": "Invalid reference"
            }
        )
    if isinstance(e, asyncpg.PostgresError):
        logger.error("Database error: %s", str(e))
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error_code": ErrorCode.DATABASE_ERROR.value,
                "error_type": ErrorType.INTERNAL.value,
                "message": "Database error"
            }
        )
    logger.exception("Unexpected error: %s", str(e))
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail={
            "error_code": ErrorCode.INTERNAL_ERROR.value,
            "error_type": ErrorType.INTERNAL.value,
            "message": "Internal server error"
        }
    )


def handle_domain_exception(e: DomainException) -> HTTPException:
    """
    Convert domain exceptions to HTTP exceptions.
    
    Strategy Pattern: Delegates to exception's to_http() method.
    Open/Closed Principle: No need to modify this when adding new exceptions.
    """
    return e.to_http()