"""
SQLAlchemy ORM models for Neon PostgreSQL (declarative style).
Tables: music_halls, music_hall_recommendations.
"""
from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Declarative base for all ORM models."""
    pass


class MusicHallModel(Base):
    """ORM model for music_halls table."""

    __tablename__ = "music_halls"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    hall_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    stage: Mapped[bool] = mapped_column(Boolean, nullable=False)
    pipe_height: Mapped[int] = mapped_column(Integer, nullable=False)
    stage_type: Mapped[str] = mapped_column(String(20), nullable=False)

    recommendations: Mapped[list["MusicHallRecommendationModel"]] = relationship(
        "MusicHallRecommendationModel",
        back_populates="hall",
        lazy="selectin",
    )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "city": self.city,
            "hall_name": self.hall_name,
            "email": self.email,
            "stage": self.stage,
            "pipe_height": self.pipe_height,
            "stage_type": self.stage_type,
        }


class MusicHallRecommendationModel(Base):
    """
    ORM model for music_hall_recommendations table.
    Composite PK (hall_id, recommendation, update_date); no surrogate id.
    """

    __tablename__ = "music_hall_recommendations"

    hall_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("music_halls.id", ondelete="CASCADE"),
        primary_key=True,
        nullable=False,
    )
    recommendation: Mapped[str] = mapped_column(Text, primary_key=True, nullable=False)
    update_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )

    hall: Mapped["MusicHallModel"] = relationship(
        "MusicHallModel", back_populates="recommendations"
    )

    def to_dict(self) -> dict:
        return {
            "recommendation": self.recommendation,
            "update_date": self.update_date.date() if self.update_date else None,
        }
