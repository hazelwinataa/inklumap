# STANDARD LIBRARY

from typing import Literal


# THIRD-PARTY LIBRARIES

from pydantic import BaseModel, Field


class AnalyticsSummaryResponse(BaseModel):
    model_version: str
    model_name: str
    silhouette_score: float | None

    total_students: int
    cluster_count: int

    high_priority: int
    medium_priority: int
    low_priority: int

    critical_access: int
    dbscan_unique_cases: int
    needs_human_review: int


class ClusterProfileResponse(BaseModel):
    id: int
    cluster_number: int

    model_version: str
    model_name: str
    distance_metric: str
    linkage: str

    cluster_name: str
    dominant_need: str
    description: str

    recommendations: list[str] = Field(
        default_factory=list,
    )

    medoid_student_code: str | None

    cluster_size: int
    mean_medoid_distance: float | None
    model_silhouette_score: float | None


class BudgetPriorityItemResponse(BaseModel):
    rank: int

    cluster_number: int
    cluster_name: str
    dominant_need: str
    description: str

    total_students: int
    high_priority: int
    medium_priority: int
    low_priority: int

    critical_access: int
    needs_human_review: int

    priority_points: int
    priority_share_percentage: float
    urgency_index: float

    urgency_level: Literal[
        "high",
        "medium",
        "low",
    ]

    recommended_actions: list[str] = Field(
        default_factory=list,
    )

    rationale: str


class BudgetPriorityResponse(BaseModel):
    model_version: str
    model_name: str

    total_students: int
    total_priority_points: int

    methodology: str
    budget_note: str

    items: list[
        BudgetPriorityItemResponse
    ] = Field(
        default_factory=list,
    )


class AnalyticsStudentListItemResponse(BaseModel):
    student_id: int
    student_code: str
    initials: str | None
    grade_level: str | None
    class_name: str | None

    assessment_id: int
    cluster_result_id: int

    cluster_number: int
    cluster_name: str

    priority_level: str

    dominant_needs: list[str] = Field(
        default_factory=list,
    )

    critical_access_flag: bool
    dbscan_unique_case: bool
    needs_human_review: bool

    individual_silhouette: float
    mean_distance_to_cluster: float


class AnalyticsStudentListResponse(BaseModel):
    total: int
    skip: int
    limit: int

    items: list[
        AnalyticsStudentListItemResponse
    ]


class AnalyticsStudentDetailResponse(
    AnalyticsStudentListItemResponse
):
    model_version: str

    maximum_need_score: int
    average_need_score: float
    critical_domain_count: int
    high_domain_count: int

    critical_access_domains: list[str] = Field(
        default_factory=list,
    )

    human_review_reason: str | None

    priority_action: str | None

    cluster_recommendations: list[str] = Field(
        default_factory=list,
    )

    individual_recommendations: list[str] = Field(
        default_factory=list,
    )

    material_preference: str | None
    assistive_tool: str | None

    recommendation_status: str | None