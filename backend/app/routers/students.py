from typing import Literal

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
from sqlalchemy.orm import (
    Session,
    selectinload,
)

from app.database import get_db
from app.models import (
    Assessment,
    AssessmentScore,
    Student,
)
from app.schemas.student import (
    StudentDetailResponse,
    StudentListResponse,
    StudentSummaryResponse,
)


router = APIRouter(
    prefix="/api/students",
    tags=["Students"],
)


@router.get(
    "/summary",
    response_model=StudentSummaryResponse,
    summary="Mendapatkan ringkasan data siswa",
)
def get_student_summary(
    database: Session = Depends(get_db),
) -> StudentSummaryResponse:
    student_counts = database.execute(
        select(
            func.count(
                Student.id
            ).label(
                "total_students"
            ),
            func.sum(
                case(
                    (
                        Student.assessment_status
                        == "complete",
                        1,
                    ),
                    else_=0,
                )
            ).label(
                "complete"
            ),
            func.sum(
                case(
                    (
                        Student.assessment_status
                        == "incomplete",
                        1,
                    ),
                    else_=0,
                )
            ).label(
                "incomplete"
            ),
            func.sum(
                case(
                    (
                        Student.assessment_status
                        == "not_started",
                        1,
                    ),
                    else_=0,
                )
            ).label(
                "not_started"
            ),
        )
    ).mappings().one()

    total_assessments = (
        database.scalar(
            select(
                func.count(
                    Assessment.id
                )
            )
        )
        or 0
    )

    total_scores = (
        database.scalar(
            select(
                func.count(
                    AssessmentScore.id
                )
            )
        )
        or 0
    )

    return StudentSummaryResponse(
        total_students=int(
            student_counts["total_students"]
            or 0
        ),
        complete=int(
            student_counts["complete"]
            or 0
        ),
        incomplete=int(
            student_counts["incomplete"]
            or 0
        ),
        not_started=int(
            student_counts["not_started"]
            or 0
        ),
        total_assessments=int(
            total_assessments
        ),
        total_scores=int(
            total_scores
        ),
    )


@router.get(
    "",
    response_model=StudentListResponse,
    summary="Mendapatkan daftar siswa",
)
def get_students(
    assessment_status: Literal[
        "complete",
        "incomplete",
        "not_started",
    ]
    | None = Query(
        default=None,
        alias="status",
        description=(
            "Filter berdasarkan status asesmen."
        ),
    ),
    grade_level: str | None = Query(
        default=None,
        description=(
            "Filter berdasarkan jenjang siswa."
        ),
    ),
    class_name: str | None = Query(
        default=None,
        description=(
            "Filter berdasarkan kelas siswa."
        ),
    ),
    search: str | None = Query(
        default=None,
        min_length=1,
        max_length=50,
        description=(
            "Pencarian berdasarkan kode "
            "atau inisial siswa."
        ),
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
) -> StudentListResponse:
    conditions = []

    if assessment_status is not None:
        conditions.append(
            Student.assessment_status
            == assessment_status
        )

    if grade_level is not None:
        conditions.append(
            Student.grade_level
            == grade_level
        )

    if class_name is not None:
        conditions.append(
            Student.class_name
            == class_name
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

    total_statement = select(
        func.count(
            Student.id
        )
    )

    if conditions:
        total_statement = (
            total_statement.where(
                *conditions
            )
        )

    total = (
        database.scalar(
            total_statement
        )
        or 0
    )

    student_statement = (
        select(Student)
        .order_by(
            Student.student_code
        )
        .offset(skip)
        .limit(limit)
    )

    if conditions:
        student_statement = (
            student_statement.where(
                *conditions
            )
        )

    students = database.scalars(
        student_statement
    ).all()

    return StudentListResponse(
        total=int(total),
        skip=skip,
        limit=limit,
        items=list(students),
    )


@router.get(
    "/{student_id}",
    response_model=StudentDetailResponse,
    summary="Mendapatkan detail siswa",
)
def get_student_detail(
    student_id: int,
    database: Session = Depends(get_db),
) -> Student:
    statement = (
        select(Student)
        .options(
            selectinload(
                Student.assessments
            ).selectinload(
                Assessment.score
            )
        )
        .where(
            Student.id == student_id
        )
    )

    student = database.scalar(
        statement
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Data siswa tidak ditemukan."
            ),
        )

    return student