from pydantic import BaseModel
from typing import Optional


# Define the request body model for the music hall data
class MusicHall(BaseModel):
    city: str
    hall_name: str
    email: str
    stage: bool
    pipe_height: int
    stage_type: str

    class Config:
        from_attributes = True  # To make Pydantic work well with ORM models


class UpdateMusicHall(BaseModel):
    city: Optional[str] = None
    hall_name: Optional[str] = None
    email: Optional[str] = None
    stage: Optional[bool] = None
    pipe_height: Optional[int] = None
    stage_type: Optional[str] = None

    class Config:
        from_attributes = True  # To make Pydantic work well with ORM models
