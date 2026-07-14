from __future__ import annotations

from datetime import date, datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.assessment_score import AssessmentScore
    from app.models.student import Student
    from app.models.user import User


class Assessment(Base):
    __tablename__ = "assessments"

    __table_args__ = (
        CheckConstraint(
            "status IN ('draft', 'submitted', 'validated')",
            name="ck_assessments_status",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    student_id: Mapped[int] = mapped_column(
        ForeignKey(
            "students.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    assessor_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
        nullable=True,
        index=True,
    )

    assessment_date: Mapped[date] = mapped_column(
        Date,
        default=date.today,
        nullable=False,
    )

    source_information: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="draft",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    student: Mapped["Student"] = relationship(
        back_populates="assessments",
    )

    assessor: Mapped["User | None"] = relationship(
        back_populates="assessments",
    )

    score: Mapped["AssessmentScore | None"] = relationship(
        back_populates="assessment",
        cascade="all, delete-orphan",
        uselist=False,
    )