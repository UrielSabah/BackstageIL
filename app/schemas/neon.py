from pydantic import BaseModel , Field, EmailStr
from enum import Enum
from typing import Optional

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

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "city": "Tel Aviv",
                "hall_name": "Barby",
                "email": "info@barby.com",
                "stage": True,
                "pipe_height": 30,
                "stage_type": "raised"
            }
        }

class UpdateMusicHall(BaseModel):
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    hall_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    stage: Optional[bool] = None
    pipe_height: Optional[int] = Field(None, ge=0, le=100)
    stage_type: Optional[StageType] = None

    class Config:
        from_attributes = True