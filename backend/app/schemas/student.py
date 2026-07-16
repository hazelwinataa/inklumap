from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class AssessmentScoreResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    visual_score: int | None
    hearing_score: int | None
    communication_score: int | None
    instruction_score: int | None
    attention_score: int | None
    mobility_score: int | None
    assistance_score: int | None
    evaluation_adjustment_score: int | None

    material_preferences: list[str] = Field(
        default_factory=list,
    )

    assistive_tools: list[str] = Field(
        default_factory=list,
    )


class AssessmentResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    student_id: int
    assessor_id: int | None

    assessment_date: date
    source_information: str | None
    notes: str | None
    status: str

    created_at: datetime
    updated_at: datetime

    score: AssessmentScoreResponse | None = None


class StudentListItemResponse(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
    student_code: str
    initials: str | None
    grade_level: str | None
    class_name: str | None
    semester: str | None
    school_year: str | None
    assessment_status: str

    created_at: datetime
    updated_at: datetime


class StudentDetailResponse(
    StudentListItemResponse
):
    assessments: list[AssessmentResponse] = Field(
        default_factory=list,
    )


class StudentListResponse(BaseModel):
    total: int
    skip: int
    limit: int
    items: list[StudentListItemResponse]


class StudentSummaryResponse(BaseModel):
    total_students: int
    complete: int
    incomplete: int
    not_started: int
    total_assessments: int
    total_scores: int