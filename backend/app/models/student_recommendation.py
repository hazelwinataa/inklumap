from __future__ import annotations


# STANDARD LIBRARY

from datetime import datetime, timezone
from typing import TYPE_CHECKING


# THIRD-PARTY LIBRARIES

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)


# LOCAL IMPORTS

from app.database import Base


if TYPE_CHECKING:
    from app.models.student_cluster_result import (
        StudentClusterResult,
    )
    from app.models.user import User


class StudentRecommendation(Base):
    __tablename__ = "student_recommendations"

    __table_args__ = (
        CheckConstraint(
            (
                "recommendation_status IN "
                "('generated', 'reviewed', "
                "'approved', 'rejected')"
            ),
            name=(
                "ck_student_recommendations_"
                "status"
            ),
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    cluster_result_id: Mapped[int] = (
        mapped_column(
            ForeignKey(
                "student_cluster_results.id",
                ondelete="CASCADE",
            ),
            unique=True,
            nullable=False,
            index=True,
        )
    )

    priority_action: Mapped[str] = (
        mapped_column(
            Text,
            nullable=False,
        )
    )

    cluster_recommendations: Mapped[
        list[str]
    ] = mapped_column(
        MutableList.as_mutable(JSONB),
        default=list,
        nullable=False,
    )

    individual_recommendations: Mapped[
        list[str]
    ] = mapped_column(
        MutableList.as_mutable(JSONB),
        default=list,
        nullable=False,
    )

    material_preference: Mapped[
        str | None
    ] = mapped_column(
        String(200),
        nullable=True,
    )

    assistive_tool: Mapped[
        str | None
    ] = mapped_column(
        String(200),
        nullable=True,
    )

    recommendation_status: Mapped[str] = (
        mapped_column(
            String(20),
            default="generated",
            nullable=False,
            index=True,
        )
    )

    reviewer_id: Mapped[int | None] = (
        mapped_column(
            ForeignKey(
                "users.id",
                ondelete="SET NULL",
            ),
            nullable=True,
            index=True,
        )
    )

    reviewer_notes: Mapped[
        str | None
    ] = mapped_column(
        Text,
        nullable=True,
    )

    reviewed_at: Mapped[
        datetime | None
    ] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(
            timezone.utc
        ),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(
            timezone.utc
        ),
        onupdate=lambda: datetime.now(
            timezone.utc
        ),
        nullable=False,
    )

    cluster_result: Mapped[
        "StudentClusterResult"
    ] = relationship(
        back_populates="recommendation",
    )

    reviewer: Mapped[
        "User | None"
    ] = relationship()