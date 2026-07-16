# THIRD-PARTY LIBRARIES

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)
from sqlalchemy import (
    delete,
    select,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import (
    Session,
    selectinload,
)


# LOCAL IMPORTS

from app.database import get_db
from app.models import (
    Assessment,
    AssessmentScore,
    Student,
    StudentClusterResult,
    User,
)
from app.schemas.assessment import (
    AssessmentCreateRequest,
    AssessmentMutationResponse,
    AssessmentReplaceRequest,
    AssessmentUpdateRequest,
    SCORE_FIELD_NAMES,
)
from app.schemas.student import (
    AssessmentResponse,
)


router = APIRouter(
    prefix="/api/assessments",
    tags=["Assessments"],
)


def get_assessment_or_404(
    database: Session,
    assessment_id: int,
) -> Assessment:
    statement = (
        select(Assessment)
        .options(
            selectinload(
                Assessment.score
            )
        )
        .where(
            Assessment.id == assessment_id
        )
    )

    assessment = database.scalar(
        statement
    )

    if assessment is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Data asesmen tidak ditemukan."
            ),
        )

    return assessment


def ensure_assessor_exists(
    database: Session,
    assessor_id: int | None,
) -> None:
    if assessor_id is None:
        return

    assessor = database.get(
        User,
        assessor_id,
    )

    if assessor is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Data penilai tidak ditemukan."
            ),
        )


def score_to_dictionary(
    score: AssessmentScore | None,
) -> dict[str, object] | None:
    if score is None:
        return None

    result: dict[str, object] = {
        field_name: getattr(
            score,
            field_name,
        )
        for field_name in SCORE_FIELD_NAMES
    }

    result["material_preferences"] = list(
        score.material_preferences or []
    )

    result["assistive_tools"] = list(
        score.assistive_tools or []
    )

    return result


def empty_score_dictionary() -> dict[str, object]:
    result: dict[str, object] = {
        field_name: None
        for field_name in SCORE_FIELD_NAMES
    }

    result["material_preferences"] = []
    result["assistive_tools"] = []

    return result


def validate_score_for_status(
    assessment_status: str,
    score_values: (
        dict[str, object] | None
    ),
) -> None:
    if assessment_status == "draft":
        return

    if score_values is None:
        raise HTTPException(
            status_code=422,
            detail=(
                "Asesmen submitted atau "
                "validated wajib memiliki skor."
            ),
        )

    missing_fields = [
        field_name
        for field_name in SCORE_FIELD_NAMES
        if score_values.get(
            field_name
        ) is None
    ]

    if missing_fields:
        raise HTTPException(
            status_code=422,
            detail=(
                "Seluruh delapan skor wajib "
                "diisi sebelum asesmen "
                "disubmit atau divalidasi. "
                "Kolom belum lengkap: "
                + ", ".join(missing_fields)
            ),
        )


def replace_assessment_score(
    assessment: Assessment,
    score_values: (
        dict[str, object] | None
    ),
) -> None:
    if score_values is None:
        assessment.score = None
        return

    if assessment.score is None:
        assessment.score = AssessmentScore(
            **score_values
        )
        return

    for field_name, value in (
        score_values.items()
    ):
        setattr(
            assessment.score,
            field_name,
            value,
        )


def patch_assessment_score(
    assessment: Assessment,
    score_values: (
        dict[str, object] | None
    ),
) -> None:
    if score_values is None:
        assessment.score = None
        return

    if assessment.score is None:
        initial_values = (
            empty_score_dictionary()
        )

        initial_values.update(
            score_values
        )

        assessment.score = AssessmentScore(
            **initial_values
        )

        return

    for field_name, value in (
        score_values.items()
    ):
        setattr(
            assessment.score,
            field_name,
            value,
        )


def is_score_complete(
    score: AssessmentScore | None,
) -> bool:
    if score is None:
        return False

    return all(
        getattr(
            score,
            field_name,
        ) is not None
        for field_name in SCORE_FIELD_NAMES
    )


def update_student_assessment_status(
    database: Session,
    student_id: int,
) -> str:
    statement = (
        select(Assessment)
        .options(
            selectinload(
                Assessment.score
            )
        )
        .where(
            Assessment.student_id
            == student_id
        )
        .order_by(
            Assessment.assessment_date.desc(),
            Assessment.id.desc(),
        )
        .limit(1)
    )

    latest_assessment = database.scalar(
        statement
    )

    student = database.get(
        Student,
        student_id,
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Data siswa tidak ditemukan."
            ),
        )

    if latest_assessment is None:
        new_status = "not_started"

    elif (
        latest_assessment.status
        in {"submitted", "validated"}
        and is_score_complete(
            latest_assessment.score
        )
    ):
        new_status = "complete"

    else:
        new_status = "incomplete"

    student.assessment_status = new_status

    return new_status


def invalidate_assessment_analytics(
    database: Session,
    assessment_id: int,
) -> bool:
    delete_result = database.execute(
        delete(
            StudentClusterResult
        ).where(
            StudentClusterResult.assessment_id
            == assessment_id
        )
    )

    deleted_count = (
        delete_result.rowcount or 0
    )

    return deleted_count > 0


def build_mutation_response(
    assessment: Assessment,
    student_status: str,
    analytics_invalidated: bool,
) -> AssessmentMutationResponse:
    return AssessmentMutationResponse(
        assessment=(
            AssessmentResponse.model_validate(
                assessment
            )
        ),
        student_assessment_status=(
            student_status
        ),
        analytics_invalidated=(
            analytics_invalidated
        ),
    )


@router.get(
    "/{assessment_id}",
    response_model=AssessmentResponse,
    summary="Mendapatkan detail asesmen",
)
def get_assessment_detail(
    assessment_id: int,
    database: Session = Depends(get_db),
) -> Assessment:
    return get_assessment_or_404(
        database,
        assessment_id,
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=AssessmentMutationResponse,
    summary="Membuat asesmen siswa",
)
def create_assessment(
    payload: AssessmentCreateRequest,
    database: Session = Depends(get_db),
) -> AssessmentMutationResponse:
    student = database.get(
        Student,
        payload.student_id,
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Data siswa tidak ditemukan."
            ),
        )

    ensure_assessor_exists(
        database,
        payload.assessor_id,
    )

    score_values = (
        payload.score.model_dump()
        if payload.score is not None
        else None
    )

    validate_score_for_status(
        payload.status,
        score_values,
    )

    assessment = Assessment(
        student_id=payload.student_id,
        assessor_id=payload.assessor_id,
        assessment_date=(
            payload.assessment_date
        ),
        source_information=(
            payload.source_information
        ),
        notes=payload.notes,
        status=payload.status,
    )

    if score_values is not None:
        assessment.score = AssessmentScore(
            **score_values
        )

    database.add(assessment)

    try:
        database.flush()

        student_status = (
            update_student_assessment_status(
                database,
                payload.student_id,
            )
        )

        database.commit()

    except IntegrityError as error:
        database.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "Asesmen gagal disimpan karena "
                "terjadi konflik data."
            ),
        ) from error

    refreshed_assessment = (
        get_assessment_or_404(
            database,
            assessment.id,
        )
    )

    return build_mutation_response(
        assessment=refreshed_assessment,
        student_status=student_status,
        analytics_invalidated=False,
    )


@router.put(
    "/{assessment_id}",
    response_model=AssessmentMutationResponse,
    summary="Mengganti seluruh data asesmen",
)
def replace_assessment(
    assessment_id: int,
    payload: AssessmentReplaceRequest,
    database: Session = Depends(get_db),
) -> AssessmentMutationResponse:
    assessment = get_assessment_or_404(
        database,
        assessment_id,
    )

    ensure_assessor_exists(
        database,
        payload.assessor_id,
    )

    score_values = (
        payload.score.model_dump()
        if payload.score is not None
        else None
    )

    validate_score_for_status(
        payload.status,
        score_values,
    )

    assessment.assessor_id = (
        payload.assessor_id
    )

    assessment.assessment_date = (
        payload.assessment_date
    )

    assessment.source_information = (
        payload.source_information
    )

    assessment.notes = payload.notes
    assessment.status = payload.status

    replace_assessment_score(
        assessment,
        score_values,
    )

    analytics_invalidated = (
        invalidate_assessment_analytics(
            database,
            assessment.id,
        )
    )

    try:
        database.flush()

        student_status = (
            update_student_assessment_status(
                database,
                assessment.student_id,
            )
        )

        database.commit()

    except IntegrityError as error:
        database.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "Asesmen gagal diperbarui karena "
                "terjadi konflik data."
            ),
        ) from error

    refreshed_assessment = (
        get_assessment_or_404(
            database,
            assessment.id,
        )
    )

    return build_mutation_response(
        assessment=refreshed_assessment,
        student_status=student_status,
        analytics_invalidated=(
            analytics_invalidated
        ),
    )


@router.patch(
    "/{assessment_id}",
    response_model=AssessmentMutationResponse,
    summary="Memperbarui sebagian data asesmen",
)
def update_assessment(
    assessment_id: int,
    payload: AssessmentUpdateRequest,
    database: Session = Depends(get_db),
) -> AssessmentMutationResponse:
    assessment = get_assessment_or_404(
        database,
        assessment_id,
    )

    update_fields = payload.model_fields_set

    if "assessor_id" in update_fields:
        ensure_assessor_exists(
            database,
            payload.assessor_id,
        )

    prospective_status = (
        payload.status
        if "status" in update_fields
        else assessment.status
    )

    current_score_values = (
        score_to_dictionary(
            assessment.score
        )
    )

    prospective_score_values = (
        current_score_values
    )

    score_patch_values: (
        dict[str, object] | None
    ) = None

    if "score" in update_fields:
        if payload.score is None:
            prospective_score_values = None
        else:
            score_patch_values = (
                payload.score.model_dump(
                    exclude_unset=True
                )
            )

            prospective_score_values = (
                current_score_values
                or empty_score_dictionary()
            )

            prospective_score_values.update(
                score_patch_values
            )

    validate_score_for_status(
        prospective_status,
        prospective_score_values,
    )

    if "assessor_id" in update_fields:
        assessment.assessor_id = (
            payload.assessor_id
        )

    if "assessment_date" in update_fields:
        assessment.assessment_date = (
            payload.assessment_date
        )

    if (
        "source_information"
        in update_fields
    ):
        assessment.source_information = (
            payload.source_information
        )

    if "notes" in update_fields:
        assessment.notes = payload.notes

    if "status" in update_fields:
        assessment.status = (
            prospective_status
        )

    if "score" in update_fields:
        patch_assessment_score(
            assessment,
            score_patch_values
            if payload.score is not None
            else None,
        )

    analytics_fields = {
        "assessment_date",
        "status",
        "score",
    }

    analytics_invalidated = False

    if analytics_fields.intersection(
        update_fields
    ):
        analytics_invalidated = (
            invalidate_assessment_analytics(
                database,
                assessment.id,
            )
        )

    try:
        database.flush()

        student_status = (
            update_student_assessment_status(
                database,
                assessment.student_id,
            )
        )

        database.commit()

    except IntegrityError as error:
        database.rollback()

        raise HTTPException(
            status_code=409,
            detail=(
                "Asesmen gagal diperbarui karena "
                "terjadi konflik data."
            ),
        ) from error

    refreshed_assessment = (
        get_assessment_or_404(
            database,
            assessment.id,
        )
    )

    return build_mutation_response(
        assessment=refreshed_assessment,
        student_status=student_status,
        analytics_invalidated=(
            analytics_invalidated
        ),
    )