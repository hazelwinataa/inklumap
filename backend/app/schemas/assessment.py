# STANDARD LIBRARY

from datetime import date
from typing import Literal


# THIRD-PARTY LIBRARIES

from pydantic import (
    BaseModel,
    Field,
    field_validator,
    model_validator,
)


# LOCAL IMPORTS

from app.schemas.student import AssessmentResponse


AssessmentStatus = Literal[
    "draft",
    "submitted",
    "validated",
]

StudentAssessmentStatus = Literal[
    "not_started",
    "incomplete",
    "complete",
]


SCORE_FIELD_NAMES = (
    "visual_score",
    "hearing_score",
    "communication_score",
    "instruction_score",
    "attention_score",
    "mobility_score",
    "assistance_score",
    "evaluation_adjustment_score",
)


def clean_string_list(
    values: list[str],
) -> list[str]:
    cleaned_values: list[str] = []

    for value in values:
        cleaned_value = value.strip()

        if not cleaned_value:
            continue

        if len(cleaned_value) > 100:
            raise ValueError(
                "Setiap pilihan maksimal "
                "100 karakter."
            )

        if cleaned_value not in cleaned_values:
            cleaned_values.append(
                cleaned_value
            )

    return cleaned_values


def validate_complete_score(
    status: AssessmentStatus,
    score: "AssessmentScoreInput | None",
) -> None:
    if status == "draft":
        return

    if score is None:
        raise ValueError(
            "Asesmen submitted atau validated "
            "wajib memiliki skor."
        )

    missing_fields = [
        field_name
        for field_name in SCORE_FIELD_NAMES
        if getattr(
            score,
            field_name,
        ) is None
    ]

    if missing_fields:
        raise ValueError(
            "Seluruh delapan skor wajib diisi "
            "untuk asesmen submitted atau "
            "validated. Kolom belum lengkap: "
            + ", ".join(missing_fields)
        )


class AssessmentScoreInput(BaseModel):
    visual_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    hearing_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    communication_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    instruction_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    attention_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    mobility_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    assistance_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    evaluation_adjustment_score: (
        int | None
    ) = Field(
        default=None,
        ge=0,
        le=3,
    )

    material_preferences: list[str] = Field(
        default_factory=list,
        max_length=20,
    )

    assistive_tools: list[str] = Field(
        default_factory=list,
        max_length=20,
    )

    @field_validator(
        "material_preferences",
        "assistive_tools",
    )
    @classmethod
    def validate_string_lists(
        cls,
        values: list[str],
    ) -> list[str]:
        return clean_string_list(values)


class AssessmentScorePatch(BaseModel):
    visual_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    hearing_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    communication_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    instruction_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    attention_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    mobility_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    assistance_score: int | None = Field(
        default=None,
        ge=0,
        le=3,
    )

    evaluation_adjustment_score: (
        int | None
    ) = Field(
        default=None,
        ge=0,
        le=3,
    )

    material_preferences: (
        list[str] | None
    ) = Field(
        default=None,
        max_length=20,
    )

    assistive_tools: (
        list[str] | None
    ) = Field(
        default=None,
        max_length=20,
    )

    @field_validator(
        "material_preferences",
        "assistive_tools",
    )
    @classmethod
    def validate_optional_string_lists(
        cls,
        values: list[str] | None,
    ) -> list[str] | None:
        if values is None:
            return None

        return clean_string_list(values)


class AssessmentMetadataBase(BaseModel):
    assessor_id: int | None = Field(
        default=None,
        ge=1,
    )

    assessment_date: date = Field(
        default_factory=date.today,
    )

    source_information: str | None = Field(
        default=None,
        max_length=255,
    )

    notes: str | None = Field(
        default=None,
        max_length=5000,
    )

    status: AssessmentStatus = "draft"

    @field_validator(
        "source_information",
        "notes",
        mode="before",
    )
    @classmethod
    def clean_optional_text(
        cls,
        value: object,
    ) -> object:
        if not isinstance(value, str):
            return value

        cleaned_value = value.strip()

        if not cleaned_value:
            return None

        return cleaned_value


class AssessmentCreateRequest(
    AssessmentMetadataBase
):
    student_id: int = Field(
        ge=1,
    )

    score: AssessmentScoreInput | None = None

    @model_validator(mode="after")
    def validate_submission(
        self,
    ) -> "AssessmentCreateRequest":
        validate_complete_score(
            self.status,
            self.score,
        )

        return self


class AssessmentReplaceRequest(
    AssessmentMetadataBase
):
    score: AssessmentScoreInput | None = None

    @model_validator(mode="after")
    def validate_submission(
        self,
    ) -> "AssessmentReplaceRequest":
        validate_complete_score(
            self.status,
            self.score,
        )

        return self


class AssessmentUpdateRequest(BaseModel):
    assessor_id: int | None = Field(
        default=None,
        ge=1,
    )

    assessment_date: date | None = None

    source_information: str | None = Field(
        default=None,
        max_length=255,
    )

    notes: str | None = Field(
        default=None,
        max_length=5000,
    )

    status: AssessmentStatus | None = None

    score: AssessmentScorePatch | None = None

    @field_validator(
        "source_information",
        "notes",
        mode="before",
    )
    @classmethod
    def clean_optional_text(
        cls,
        value: object,
    ) -> object:
        if not isinstance(value, str):
            return value

        cleaned_value = value.strip()

        if not cleaned_value:
            return None

        return cleaned_value

    @model_validator(mode="after")
    def validate_update_fields(
        self,
    ) -> "AssessmentUpdateRequest":
        if not self.model_fields_set:
            raise ValueError(
                "Minimal satu kolom harus "
                "dikirim untuk pembaruan."
            )

        return self


class AssessmentMutationResponse(BaseModel):
    assessment: AssessmentResponse

    student_assessment_status: (
        StudentAssessmentStatus
    )

    analytics_invalidated: bool