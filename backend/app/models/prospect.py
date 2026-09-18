from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Index, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.enums import ProspectPriority, ProspectStatus


class Prospect(Base):
    __tablename__ = "prospects"
    __table_args__ = (
        Index("ix_prospects_status_priority", "status", "priority"),
        Index("ix_prospects_assigned_status", "assigned_to", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False, index=True)
    assigned_to: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    score: Mapped[float] = mapped_column(Float, default=0.0)
    priority: Mapped[str] = mapped_column(String(32), default=ProspectPriority.MEDIUM.value, index=True)
    status: Mapped[str] = mapped_column(String(32), default=ProspectStatus.NEW.value, index=True)
    notes: Mapped[str | None] = mapped_column(Text)
    estimated_value: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), onupdate=func.now())

    company = relationship("Company", back_populates="prospects")
    assigned_user = relationship("User", back_populates="assigned_prospects")
    contacts = relationship("Contact", back_populates="prospect", cascade="all, delete-orphan")
    activities = relationship("Activity", back_populates="prospect", cascade="all, delete-orphan")
    follow_ups = relationship("FollowUp", back_populates="prospect", cascade="all, delete-orphan")
    conversions = relationship("Conversion", back_populates="prospect", cascade="all, delete-orphan")
    ai_evaluations = relationship("AIEvaluation", back_populates="prospect", cascade="all, delete-orphan")
