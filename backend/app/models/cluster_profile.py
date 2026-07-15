from __future__ import annotations


# STANDARD LIBRARY

from datetime import datetime, timezone
from typing import TYPE_CHECKING


# THIRD-PARTY LIBRARIES

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
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
    from app.models.student import Student
    from app.models.student_cluster_result import (
        StudentClusterResult,
    )


class ClusterProfile(Base):
    __tablename__ = "cluster_profiles"

    __table_args__ = (
        UniqueConstraint(
            "model_version",
            "cluster_number",
            name=(
                "uq_cluster_profiles_"
                "version_number"
            ),
        ),
        CheckConstraint(
            "cluster_number > 0",
            name=(
                "ck_cluster_profiles_"
                "cluster_number"
            ),
        ),
        CheckConstraint(
            "cluster_size >= 0",
            name=(
                "ck_cluster_profiles_"
                "cluster_size"
            ),
        ),
        CheckConstraint(
            (
                "mean_medoid_distance IS NULL "
                "OR mean_medoid_distance "
                "BETWEEN 0 AND 1"
            ),
            name=(
                "ck_cluster_profiles_"
                "medoid_distance"
            ),
        ),
        CheckConstraint(
            (
                "model_silhouette_score IS NULL "
                "OR model_silhouette_score "
                "BETWEEN -1 AND 1"
            ),
            name=(
                "ck_cluster_profiles_"
                "silhouette"
            ),
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    model_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    cluster_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    model_name: Mapped[str] = mapped_column(
        String(100),
        default="hierarchical_gower",
        nullable=False,
    )

    distance_metric: Mapped[str] = mapped_column(
        String(30),
        default="gower",
        nullable=False,
    )

    linkage: Mapped[str] = mapped_column(
        String(30),
        default="average",
        nullable=False,
    )

    cluster_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    dominant_need: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    recommendations: Mapped[list[str]] = mapped_column(
        MutableList.as_mutable(JSONB),
        default=list,
        nullable=False,
    )

    medoid_student_id: Mapped[int | None] = (
        mapped_column(
            ForeignKey(
                "students.id",
                ondelete="SET NULL",
            ),
            nullable=True,
            index=True,
        )
    )

    cluster_size: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    mean_medoid_distance: Mapped[
        float | None
    ] = mapped_column(
        Float,
        nullable=True,
    )

    model_silhouette_score: Mapped[
        float | None
    ] = mapped_column(
        Float,
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

    medoid_student: Mapped[
        "Student | None"
    ] = relationship()

    student_results: Mapped[
        list["StudentClusterResult"]
    ] = relationship(
        back_populates="cluster_profile",
    )