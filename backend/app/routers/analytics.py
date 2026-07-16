# STANDARD LIBRARY

from typing import Literal


# THIRD-PARTY LIBRARIES

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from sqlalchemy import (
    case,
    func,
    or_,
    select,
)
from sqlalchemy.orm import Session


# LOCAL IMPORTS

from app.database import get_db
from app.models import (
    Assessment,
    ClusterProfile,
    Student,
    StudentClusterResult,
    StudentRecommendation,
)
from app.schemas.analytics import (
    AnalyticsStudentDetailResponse,
    AnalyticsStudentListItemResponse,
    AnalyticsStudentListResponse,
    AnalyticsSummaryResponse,
    BudgetPriorityItemResponse,
    BudgetPriorityResponse,
    ClusterProfileResponse,
)


DEFAULT_MODEL_VERSION = (
    "hierarchical_gower_v1"
)


router = APIRouter(
    prefix="/api/analytics",
    tags=["Analytics"],
)


@router.get(
    "/summary",
    response_model=AnalyticsSummaryResponse,
    summary="Mendapatkan ringkasan analytics",
)
def get_analytics_summary(
    model_version: str = Query(
        default=DEFAULT_MODEL_VERSION,
        min_length=1,
        max_length=50,
    ),
    database: Session = Depends(get_db),
) -> AnalyticsSummaryResponse:
    model_information = (
        database.execute(
            select(
                ClusterProfile.model_name,
                ClusterProfile.model_silhouette_score,
            )
            .where(
                ClusterProfile.model_version
                == model_version
            )
            .order_by(
                ClusterProfile.cluster_number
            )
            .limit(1)
        )
        .mappings()
        .one_or_none()
    )

    if model_information is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Data analytics untuk model "
                "tersebut tidak ditemukan."
            ),
        )

    summary = (
        database.execute(
            select(
                func.count(
                    StudentClusterResult.id
                ).label(
                    "total_students"
                ),
                func.count(
                    func.distinct(
                        StudentClusterResult
                        .cluster_profile_id
                    )
                ).label(
                    "cluster_count"
                ),
                func.sum(
                    case(
                        (
                            StudentClusterResult
                            .priority_level
                            == "high",
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "high_priority"
                ),
                func.sum(
                    case(
                        (
                            StudentClusterResult
                            .priority_level
                            == "medium",
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "medium_priority"
                ),
                func.sum(
                    case(
                        (
                            StudentClusterResult
                            .priority_level
                            == "low",
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "low_priority"
                ),
                func.sum(
                    case(
                        (
                            StudentClusterResult
                            .critical_access_flag
                            .is_(True),
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "critical_access"
                ),
                func.sum(
                    case(
                        (
                            StudentClusterResult
                            .dbscan_unique_case
                            .is_(True),
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "dbscan_unique_cases"
                ),
                func.sum(
                    case(
                        (
                            StudentClusterResult
                            .needs_human_review
                            .is_(True),
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "needs_human_review"
                ),
            ).where(
                StudentClusterResult.model_version
                == model_version
            )
        )
        .mappings()
        .one()
    )

    return AnalyticsSummaryResponse(
        model_version=model_version,
        model_name=(
            model_information[
                "model_name"
            ]
        ),
        silhouette_score=(
            model_information[
                "model_silhouette_score"
            ]
        ),
        total_students=int(
            summary["total_students"]
            or 0
        ),
        cluster_count=int(
            summary["cluster_count"]
            or 0
        ),
        high_priority=int(
            summary["high_priority"]
            or 0
        ),
        medium_priority=int(
            summary["medium_priority"]
            or 0
        ),
        low_priority=int(
            summary["low_priority"]
            or 0
        ),
        critical_access=int(
            summary["critical_access"]
            or 0
        ),
        dbscan_unique_cases=int(
            summary["dbscan_unique_cases"]
            or 0
        ),
        needs_human_review=int(
            summary["needs_human_review"]
            or 0
        ),
    )


@router.get(
    "/clusters",
    response_model=list[
        ClusterProfileResponse
    ],
    summary="Mendapatkan profil cluster",
)
def get_cluster_profiles(
    model_version: str = Query(
        default=DEFAULT_MODEL_VERSION,
        min_length=1,
        max_length=50,
    ),
    database: Session = Depends(get_db),
) -> list[ClusterProfileResponse]:
    rows = database.execute(
        select(
            ClusterProfile,
            Student.student_code.label(
                "medoid_student_code"
            ),
        )
        .outerjoin(
            Student,
            Student.id
            == ClusterProfile.medoid_student_id,
        )
        .where(
            ClusterProfile.model_version
            == model_version
        )
        .order_by(
            ClusterProfile.cluster_number
        )
    ).all()

    if not rows:
        raise HTTPException(
            status_code=404,
            detail=(
                "Profil cluster tidak ditemukan."
            ),
        )

    return [
        ClusterProfileResponse(
            id=profile.id,
            cluster_number=(
                profile.cluster_number
            ),
            model_version=(
                profile.model_version
            ),
            model_name=profile.model_name,
            distance_metric=(
                profile.distance_metric
            ),
            linkage=profile.linkage,
            cluster_name=profile.cluster_name,
            dominant_need=(
                profile.dominant_need
            ),
            description=profile.description,
            recommendations=list(
                profile.recommendations
                or []
            ),
            medoid_student_code=(
                medoid_student_code
            ),
            cluster_size=profile.cluster_size,
            mean_medoid_distance=(
                profile.mean_medoid_distance
            ),
            model_silhouette_score=(
                profile.model_silhouette_score
            ),
        )
        for profile, medoid_student_code
        in rows
    ]


@router.get(
    "/budget-priorities",
    response_model=BudgetPriorityResponse,
    summary=(
        "Mendapatkan prioritas dukungan anggaran"
    ),
)
def get_budget_priorities(
    model_version: str = Query(
        default=DEFAULT_MODEL_VERSION,
        min_length=1,
        max_length=50,
    ),
    database: Session = Depends(get_db),
) -> BudgetPriorityResponse:
    profiles = (
        database.scalars(
            select(
                ClusterProfile
            )
            .where(
                ClusterProfile.model_version
                == model_version
            )
            .order_by(
                ClusterProfile.cluster_number
            )
        )
        .all()
    )

    if not profiles:
        raise HTTPException(
            status_code=404,
            detail=(
                "Data prioritas anggaran untuk "
                "model tersebut tidak ditemukan."
            ),
        )

    aggregate_rows = (
        database.execute(
            select(
                StudentClusterResult
                .cluster_profile_id,
                func.count(
                    StudentClusterResult.id
                ).label(
                    "total_students"
                ),
                func.sum(
                    case(
                        (
                            StudentClusterResult
                            .priority_level
                            == "high",
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "high_priority"
                ),
                func.sum(
                    case(
                        (
                            StudentClusterResult
                            .priority_level
                            == "medium",
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "medium_priority"
                ),
                func.sum(
                    case(
                        (
                            StudentClusterResult
                            .priority_level
                            == "low",
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "low_priority"
                ),
                func.sum(
                    case(
                        (
                            StudentClusterResult
                            .critical_access_flag
                            .is_(True),
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "critical_access"
                ),
                func.sum(
                    case(
                        (
                            StudentClusterResult
                            .needs_human_review
                            .is_(True),
                            1,
                        ),
                        else_=0,
                    )
                ).label(
                    "needs_human_review"
                ),
            )
            .where(
                StudentClusterResult.model_version
                == model_version
            )
            .group_by(
                StudentClusterResult
                .cluster_profile_id
            )
        )
        .mappings()
        .all()
    )

    aggregates_by_profile = {
        int(row["cluster_profile_id"]): row
        for row in aggregate_rows
    }

    calculated_items: list[dict] = []

    for profile in profiles:
        aggregate = aggregates_by_profile.get(
            profile.id
        )

        total_students = int(
            aggregate["total_students"]
            if aggregate is not None
            else 0
        )
        high_priority = int(
            aggregate["high_priority"]
            if aggregate is not None
            else 0
        )
        medium_priority = int(
            aggregate["medium_priority"]
            if aggregate is not None
            else 0
        )
        low_priority = int(
            aggregate["low_priority"]
            if aggregate is not None
            else 0
        )
        critical_access = int(
            aggregate["critical_access"]
            if aggregate is not None
            else 0
        )
        needs_human_review = int(
            aggregate["needs_human_review"]
            if aggregate is not None
            else 0
        )

        priority_points = (
            (high_priority * 3)
            + (medium_priority * 2)
            + low_priority
            + (critical_access * 2)
            + needs_human_review
        )

        maximum_points = (
            total_students * 6
        )

        urgency_index = (
            round(
                (
                    priority_points
                    / maximum_points
                    * 100
                ),
                2,
            )
            if maximum_points > 0
            else 0.0
        )

        if urgency_index >= 60:
            urgency_level = "high"
        elif urgency_index >= 40:
            urgency_level = "medium"
        else:
            urgency_level = "low"

        calculated_items.append(
            {
                "cluster_number": (
                    profile.cluster_number
                ),
                "cluster_name": (
                    profile.cluster_name
                ),
                "dominant_need": (
                    profile.dominant_need
                ),
                "description": (
                    profile.description
                ),
                "total_students": (
                    total_students
                ),
                "high_priority": (
                    high_priority
                ),
                "medium_priority": (
                    medium_priority
                ),
                "low_priority": low_priority,
                "critical_access": (
                    critical_access
                ),
                "needs_human_review": (
                    needs_human_review
                ),
                "priority_points": (
                    priority_points
                ),
                "urgency_index": (
                    urgency_index
                ),
                "urgency_level": (
                    urgency_level
                ),
                "recommended_actions": list(
                    profile.recommendations
                    or []
                ),
                "rationale": (
                    "Prioritas dihitung dari "
                    f"{total_students} siswa: "
                    f"{high_priority} prioritas "
                    "tinggi, "
                    f"{critical_access} hambatan "
                    "akses kritis, dan "
                    f"{needs_human_review} hasil "
                    "yang memerlukan validasi "
                    "guru."
                ),
            }
        )

    calculated_items.sort(
        key=lambda item: (
            -item["priority_points"],
            item["cluster_number"],
        )
    )

    total_priority_points = sum(
        item["priority_points"]
        for item in calculated_items
    )

    response_items = [
        BudgetPriorityItemResponse(
            rank=index,
            priority_share_percentage=(
                round(
                    (
                        item["priority_points"]
                        / total_priority_points
                        * 100
                    ),
                    2,
                )
                if total_priority_points > 0
                else 0.0
            ),
            **item,
        )
        for index, item
        in enumerate(
            calculated_items,
            start=1,
        )
    ]

    model_name = profiles[0].model_name

    return BudgetPriorityResponse(
        model_version=model_version,
        model_name=model_name,
        total_students=sum(
            item.total_students
            for item in response_items
        ),
        total_priority_points=(
            total_priority_points
        ),
        methodology=(
            "Skor prioritas = 3 x jumlah "
            "prioritas tinggi + 2 x prioritas "
            "sedang + 1 x prioritas rendah + "
            "2 x akses kritis + 1 x kebutuhan "
            "validasi guru."
        ),
        budget_note=(
            "Nilai ini digunakan untuk "
            "pemeringkatan kebutuhan sumber "
            "daya dan bukan estimasi nominal "
            "biaya."
        ),
        items=response_items,
    )


@router.get(
    "/students",
    response_model=AnalyticsStudentListResponse,
    summary=(
        "Mendapatkan daftar hasil analytics siswa"
    ),
)
def get_analytics_students(
    model_version: str = Query(
        default=DEFAULT_MODEL_VERSION,
        min_length=1,
        max_length=50,
    ),
    cluster_number: int | None = Query(
        default=None,
        ge=1,
    ),
    priority_level: Literal[
        "high",
        "medium",
        "low",
    ]
    | None = Query(
        default=None,
    ),
    critical_access: bool | None = Query(
        default=None,
    ),
    needs_review: bool | None = Query(
        default=None,
    ),
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=50,
    ),
    skip: int = Query(
        default=0,
        ge=0,
    ),
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
    database: Session = Depends(get_db),
) -> AnalyticsStudentListResponse:
    conditions = [
        StudentClusterResult.model_version
        == model_version
    ]

    if cluster_number is not None:
        conditions.append(
            ClusterProfile.cluster_number
            == cluster_number
        )

    if priority_level is not None:
        conditions.append(
            StudentClusterResult.priority_level
            == priority_level
        )

    if critical_access is not None:
        conditions.append(
            StudentClusterResult
            .critical_access_flag
            == critical_access
        )

    if needs_review is not None:
        conditions.append(
            StudentClusterResult
            .needs_human_review
            == needs_review
        )

    if search is not None:
        cleaned_search = search.strip()

        if cleaned_search:
            search_pattern = (
                f"%{cleaned_search}%"
            )

            conditions.append(
                or_(
                    Student.student_code.ilike(
                        search_pattern
                    ),
                    Student.initials.ilike(
                        search_pattern
                    ),
                )
            )

    count_statement = (
        select(
            func.count(
                StudentClusterResult.id
            )
        )
        .join(
            Assessment,
            Assessment.id
            == StudentClusterResult.assessment_id,
        )
        .join(
            Student,
            Student.id
            == Assessment.student_id,
        )
        .join(
            ClusterProfile,
            ClusterProfile.id
            == StudentClusterResult
            .cluster_profile_id,
        )
        .where(
            *conditions
        )
    )

    total = (
        database.scalar(
            count_statement
        )
        or 0
    )

    statement = (
        select(
            Student,
            Assessment,
            StudentClusterResult,
            ClusterProfile,
        )
        .join(
            Assessment,
            Assessment.id
            == StudentClusterResult.assessment_id,
        )
        .join(
            Student,
            Student.id
            == Assessment.student_id,
        )
        .join(
            ClusterProfile,
            ClusterProfile.id
            == StudentClusterResult
            .cluster_profile_id,
        )
        .where(
            *conditions
        )
        .order_by(
            Student.student_code
        )
        .offset(skip)
        .limit(limit)
    )

    rows = database.execute(
        statement
    ).all()

    items = [
        AnalyticsStudentListItemResponse(
            student_id=student.id,
            student_code=student.student_code,
            initials=student.initials,
            grade_level=student.grade_level,
            class_name=student.class_name,
            assessment_id=assessment.id,
            cluster_result_id=result.id,
            cluster_number=(
                cluster.cluster_number
            ),
            cluster_name=cluster.cluster_name,
            priority_level=(
                result.priority_level
            ),
            dominant_needs=list(
                result.dominant_needs
                or []
            ),
            critical_access_flag=(
                result.critical_access_flag
            ),
            dbscan_unique_case=(
                result.dbscan_unique_case
            ),
            needs_human_review=(
                result.needs_human_review
            ),
            individual_silhouette=(
                result.individual_silhouette
            ),
            mean_distance_to_cluster=(
                result.mean_distance_to_cluster
            ),
        )
        for (
            student,
            assessment,
            result,
            cluster,
        ) in rows
    ]

    return AnalyticsStudentListResponse(
        total=int(total),
        skip=skip,
        limit=limit,
        items=items,
    )


@router.get(
    "/students/{student_id}",
    response_model=(
        AnalyticsStudentDetailResponse
    ),
    summary=(
        "Mendapatkan detail analytics siswa"
    ),
)
def get_analytics_student_detail(
    student_id: int,
    model_version: str = Query(
        default=DEFAULT_MODEL_VERSION,
        min_length=1,
        max_length=50,
    ),
    database: Session = Depends(get_db),
) -> AnalyticsStudentDetailResponse:
    statement = (
        select(
            Student,
            Assessment,
            StudentClusterResult,
            ClusterProfile,
            StudentRecommendation,
        )
        .join(
            Assessment,
            Assessment.student_id
            == Student.id,
        )
        .join(
            StudentClusterResult,
            StudentClusterResult.assessment_id
            == Assessment.id,
        )
        .join(
            ClusterProfile,
            ClusterProfile.id
            == StudentClusterResult
            .cluster_profile_id,
        )
        .outerjoin(
            StudentRecommendation,
            StudentRecommendation
            .cluster_result_id
            == StudentClusterResult.id,
        )
        .where(
            Student.id == student_id,
            StudentClusterResult.model_version
            == model_version,
        )
        .order_by(
            Assessment.assessment_date.desc(),
            Assessment.id.desc(),
        )
        .limit(1)
    )

    row = database.execute(
        statement
    ).one_or_none()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Hasil analytics siswa "
                "tidak ditemukan."
            ),
        )

    (
        student,
        assessment,
        result,
        cluster,
        recommendation,
    ) = row

    return AnalyticsStudentDetailResponse(
        student_id=student.id,
        student_code=student.student_code,
        initials=student.initials,
        grade_level=student.grade_level,
        class_name=student.class_name,
        assessment_id=assessment.id,
        cluster_result_id=result.id,
        cluster_number=(
            cluster.cluster_number
        ),
        cluster_name=cluster.cluster_name,
        priority_level=result.priority_level,
        dominant_needs=list(
            result.dominant_needs
            or []
        ),
        critical_access_flag=(
            result.critical_access_flag
        ),
        dbscan_unique_case=(
            result.dbscan_unique_case
        ),
        needs_human_review=(
            result.needs_human_review
        ),
        individual_silhouette=(
            result.individual_silhouette
        ),
        mean_distance_to_cluster=(
            result.mean_distance_to_cluster
        ),
        model_version=result.model_version,
        maximum_need_score=(
            result.maximum_need_score
        ),
        average_need_score=(
            result.average_need_score
        ),
        critical_domain_count=(
            result.critical_domain_count
        ),
        high_domain_count=(
            result.high_domain_count
        ),
        critical_access_domains=list(
            result.critical_access_domains
            or []
        ),
        human_review_reason=(
            result.human_review_reason
        ),
        priority_action=(
            recommendation.priority_action
            if recommendation is not None
            else None
        ),
        cluster_recommendations=(
            list(
                recommendation
                .cluster_recommendations
                or []
            )
            if recommendation is not None
            else []
        ),
        individual_recommendations=(
            list(
                recommendation
                .individual_recommendations
                or []
            )
            if recommendation is not None
            else []
        ),
        material_preference=(
            recommendation.material_preference
            if recommendation is not None
            else None
        ),
        assistive_tool=(
            recommendation.assistive_tool
            if recommendation is not None
            else None
        ),
        recommendation_status=(
            recommendation
            .recommendation_status
            if recommendation is not None
            else None
        ),
    )