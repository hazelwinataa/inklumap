from __future__ import annotations

from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.assessment import Assessment


class Student(Base):
    __tablename__ = "students"

    __table_args__ = (
        CheckConstraint(
            "assessment_status IN "
            "('not_started', 'incomplete', 'complete')",
            name="ck_students_assessment_status",
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    student_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )

    initials: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    grade_level: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    class_name: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    semester: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    school_year: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    assessment_status: Mapped[str] = mapped_column(
        String(20),
        default="not_started",
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

    assessments: Mapped[list["Assessment"]] = relationship(
        back_populates="student",
        cascade="all, delete-orphan",
    )