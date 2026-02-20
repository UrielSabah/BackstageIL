from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class StageType(str, Enum):
    open = "open"
    closed = "closed"
    portable = "portable"
    raised = "raised"


class MusicHall(BaseModel):
    city: str = Field(..., min_length=2, max_length=100, description="City where the hall is located")
    hall_name: str = Field(..., min_length=2, max_length=100, description="Name of the music hall")
    email: EmailStr = Field(..., description="Contact email")
    stage: bool = Field(..., description="Whether the hall has a stage")
    pipe_height: int = Field(..., ge=0, le=100, description="Height of the stage pipes in meters")
    stage_type: StageType = Field(...,  description="Type of stage")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "city": "Tel Aviv",
                "hall_name": "Barby",
                "email": "info@barby.com",
                "stage": True,
                "pipe_height": 30,
                "stage_type": "raised"
            }
        }
    )


class UpdateMusicHall(BaseModel):
    """Partial update; only provided fields are applied."""
    city: str | None = Field(None, min_length=2, max_length=100)
    hall_name: str | None = Field(None, min_length=2, max_length=100)
    email: EmailStr | None = None
    stage: bool | None = None
    pipe_height: int | None = Field(None, ge=0, le=100)
    stage_type: StageType | None = None

    model_config = ConfigDict(
        from_attributes=True
    )


class MusicHallResponse(MusicHall):
    """MusicHall with ID for response models"""
    id: int = Field(..., description="Unique identifier for the music hall")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "city": "Tel Aviv",
                "hall_name": "Barby",
                "email": "info@barby.com",
                "stage": True,
                "pipe_height": 30,
                "stage_type": "raised"
            }
        }
    )


class MusicHallListItem(BaseModel):
    """Simplified music hall item for list endpoints"""
    id: int = Field(..., description="Unique identifier for the music hall")
    city_and_hall_name: str = Field(..., description="Combined city and hall name")

    model_config = ConfigDict(
        from_attributes=True
    )


class MusicHallRecommendation(BaseModel):
    """Recommendation for a music hall"""
    update_date: date = Field(..., description="Date when the recommendation was last updated")
    recommendation: str = Field(..., description="Recommendation text")

    model_config = ConfigDict(
        from_attributes=True
    )