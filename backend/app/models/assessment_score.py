from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    Integer,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database import Base


if TYPE_CHECKING:
    from app.models.assessment import Assessment


class AssessmentScore(Base):
    __tablename__ = "assessment_scores"

    __table_args__ = (
        CheckConstraint(
            "visual_score BETWEEN 0 AND 3",
            name="ck_scores_visual",
        ),
        CheckConstraint(
            "hearing_score BETWEEN 0 AND 3",
            name="ck_scores_hearing",
        ),
        CheckConstraint(
            "communication_score BETWEEN 0 AND 3",
            name="ck_scores_communication",
        ),
        CheckConstraint(
            "instruction_score BETWEEN 0 AND 3",
            name="ck_scores_instruction",
        ),
        CheckConstraint(
            "attention_score BETWEEN 0 AND 3",
            name="ck_scores_attention",
        ),
        CheckConstraint(
            "mobility_score BETWEEN 0 AND 3",
            name="ck_scores_mobility",
        ),
        CheckConstraint(
            "assistance_score BETWEEN 0 AND 3",
            name="ck_scores_assistance",
        ),
        CheckConstraint(
            (
                "evaluation_adjustment_score "
                "BETWEEN 0 AND 3"
            ),
            name=(
                "ck_scores_"
                "evaluation_adjustment"
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
        unique=True,
        nullable=False,
        index=True,
    )

    visual_score: Mapped[int | None] = (
        mapped_column(
            Integer,
            nullable=True,
        )
    )

    hearing_score: Mapped[int | None] = (
        mapped_column(
            Integer,
            nullable=True,
        )
    )

    communication_score: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True,
    )

    instruction_score: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True,
    )

    attention_score: Mapped[int | None] = (
        mapped_column(
            Integer,
            nullable=True,
        )
    )

    mobility_score: Mapped[int | None] = (
        mapped_column(
            Integer,
            nullable=True,
        )
    )

    assistance_score: Mapped[int | None] = (
        mapped_column(
            Integer,
            nullable=True,
        )
    )

    evaluation_adjustment_score: Mapped[
        int | None
    ] = mapped_column(
        Integer,
        nullable=True,
    )

    material_preferences: Mapped[
        list[str]
    ] = mapped_column(
        MutableList.as_mutable(JSONB),
        default=list,
        nullable=False,
    )

    assistive_tools: Mapped[
        list[str]
    ] = mapped_column(
        MutableList.as_mutable(JSONB),
        default=list,
        nullable=False,
    )

    assessment: Mapped[
        "Assessment"
    ] = relationship(
        back_populates="score",
    )