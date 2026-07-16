"""allow partial assessment drafts

Revision ID: b7c1a9f42d6e
Revises: ededc506f636
Create Date: 2026-07-16
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b7c1a9f42d6e"

down_revision: Union[
    str,
    Sequence[str],
    None,
] = "ededc506f636"

branch_labels: Union[
    str,
    Sequence[str],
    None,
] = None

depends_on: Union[
    str,
    Sequence[str],
    None,
] = None


SCORE_COLUMNS = (
    "visual_score",
    "hearing_score",
    "communication_score",
    "instruction_score",
    "attention_score",
    "mobility_score",
    "assistance_score",
    "evaluation_adjustment_score",
)


def upgrade() -> None:
    for column_name in SCORE_COLUMNS:
        op.alter_column(
            "assessment_scores",
            column_name,
            existing_type=sa.Integer(),
            nullable=True,
        )


def downgrade() -> None:
    for column_name in SCORE_COLUMNS:
        op.execute(
            sa.text(
                f"""
                UPDATE assessment_scores
                SET {column_name} = 0
                WHERE {column_name} IS NULL
                """
            )
        )

        op.alter_column(
            "assessment_scores",
            column_name,
            existing_type=sa.Integer(),
            nullable=False,
        )