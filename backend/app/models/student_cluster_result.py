from __future__ import annotations


# STANDARD LIBRARY

from datetime import datetime, timezone
from typing import TYPE_CHECKING


# THIRD-PARTY LIBRARIES

from sqlalchemy import (
    Boolean,
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
    from app.models.assessment import Assessment
    from app.models.cluster_profile import (
        ClusterProfile,
    )
    from app.models.student_recommendation import (
        StudentRecommendation,
    )


class StudentClusterResult(Base):
    __tablename__ = "student_cluster_results"

    __table_args__ = (
        UniqueConstraint(
            "assessment_id",
            "model_version",
            name=(
                "uq_student_cluster_results_"
                "assessment_version"
            ),
        ),
        CheckConstraint(
            (
                "priority_level IN "
                "('high', 'medium', 'low')"
            ),
            name=(
                "ck_student_cluster_results_"
                "priority"
            ),
        ),
        CheckConstraint(
            "maximum_need_score BETWEEN 0 AND 3",
            name=(
                "ck_student_cluster_results_"
                "maximum_score"
            ),
        ),
        CheckConstraint(
            (
                "average_need_score "
                "BETWEEN 0 AND 3"
            ),
            name=(
                "ck_student_cluster_results_"
                "average_score"
            ),
        ),
        CheckConstraint(
            (
                "critical_domain_count "
                "BETWEEN 0 AND 8"
            ),
            name=(
                "ck_student_cluster_results_"
                "critical_count"
            ),
        ),
        CheckConstraint(
            (
                "high_domain_count "
                "BETWEEN 0 AND 8"
            ),
            name=(
                "ck_student_cluster_results_"
                "high_count"
            ),
        ),
        CheckConstraint(
            (
                "individual_silhouette "
                "BETWEEN -1 AND 1"
            ),
            name=(
                "ck_student_cluster_results_"
                "silhouette"
            ),
        ),
        CheckConstraint(
            (
                "mean_distance_to_cluster "
                "BETWEEN 0 AND 1"
            ),
            name=(
                "ck_student_cluster_results_"
                "mean_distance"
            ),
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    assessment_id: Mapped[int] = mapped_column(
        ForeignKey(
            "assessments.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    cluster_profile_id: Mapped[int] = (
        mapped_column(
            ForeignKey(
                "cluster_profiles.id",
                ondelete="RESTRICT",
            ),
            nullable=False,
            index=True,
        )
    )

    model_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True,
    )

    dominant_needs: Mapped[list[str]] = (
        mapped_column(
            MutableList.as_mutable(JSONB),
            default=list,
            nullable=False,
        )
    )

    maximum_need_score: Mapped[int] = (
        mapped_column(
            Integer,
            nullable=False,
        )
    )

    average_need_score: Mapped[float] = (
        mapped_column(
            Float,
            nullable=False,
        )
    )

    critical_domain_count: Mapped[int] = (
        mapped_column(
            Integer,
            nullable=False,
        )
    )

    high_domain_count: Mapped[int] = (
        mapped_column(
            Integer,
            nullable=False,
        )
    )

    priority_level: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )

    individual_silhouette: Mapped[float] = (
        mapped_column(
            Float,
            nullable=False,
        )
    )

    mean_distance_to_cluster: Mapped[
        float
    ] = mapped_column(
        Float,
        nullable=False,
    )

    critical_access_flag: Mapped[bool] = (
        mapped_column(
            Boolean,
            default=False,
            nullable=False,
            index=True,
        )
    )

    critical_access_domains: Mapped[
        list[str]
    ] = mapped_column(
        MutableList.as_mutable(JSONB),
        default=list,
        nullable=False,
    )

    dbscan_unique_case: Mapped[bool] = (
        mapped_column(
            Boolean,
            default=False,
            nullable=False,
            index=True,
        )
    )

    needs_human_review: Mapped[bool] = (
        mapped_column(
            Boolean,
            default=False,
            nullable=False,
            index=True,
        )
    )

    human_review_reason: Mapped[
        str | None
    ] = mapped_column(
        Text,
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

    assessment: Mapped["Assessment"] = (
        relationship()
    )

    cluster_profile: Mapped[
        "ClusterProfile"
    ] = relationship(
        back_populates="student_results",
    )

    recommendation: Mapped[
        "StudentRecommendation | None"
    ] = relationship(
        back_populates="cluster_result",
        cascade="all, delete-orphan",
        uselist=False,
    )