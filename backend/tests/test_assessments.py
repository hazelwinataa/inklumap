# STANDARD LIBRARY

from datetime import date
from typing import Any


# THIRD-PARTY LIBRARIES

from fastapi.testclient import TestClient


# HELPER FUNCTIONS

def get_student_by_code(
    client: TestClient,
    student_code: str = "SIS-001",
) -> dict[str, Any]:
    response = client.get(
        "/api/students",
        params={
            "search": student_code,
            "limit": 1,
        },
    )

    assert response.status_code == 200

    items = response.json()["items"]

    assert len(items) == 1
    assert items[0]["student_code"] == student_code

    return items[0]


def get_not_started_student(
    client: TestClient,
) -> dict[str, Any]:
    response = client.get(
        "/api/students",
        params={
            "status": "not_started",
            "limit": 1,
        },
    )

    assert response.status_code == 200

    items = response.json()["items"]

    assert len(items) == 1
    assert (
        items[0]["assessment_status"]
        == "not_started"
    )

    return items[0]


def get_latest_assessment(
    client: TestClient,
    student_code: str = "SIS-001",
) -> tuple[dict[str, Any], dict[str, Any]]:
    student = get_student_by_code(
        client,
        student_code,
    )

    response = client.get(
        f"/api/students/{student['id']}"
    )

    assert response.status_code == 200

    assessments = response.json()[
        "assessments"
    ]

    assert assessments

    latest_assessment = max(
        assessments,
        key=lambda assessment: (
            assessment["assessment_date"],
            assessment["id"],
        ),
    )

    return student, latest_assessment


def complete_score_payload() -> dict[str, Any]:
    return {
        "visual_score": 1,
        "hearing_score": 2,
        "communication_score": 1,
        "instruction_score": 2,
        "attention_score": 1,
        "mobility_score": 0,
        "assistance_score": 2,
        "evaluation_adjustment_score": 1,
        "material_preferences": [
            "Teks",
            "Visual",
        ],
        "assistive_tools": [
            "Perangkat Caption",
        ],
    }


def create_payload(
    student_id: int,
    status: str = "draft",
    score: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "student_id": student_id,
        "assessment_date": (
            date.today().isoformat()
        ),
        "source_information": (
            "Observasi guru dan diskusi kelas"
        ),
        "notes": (
            "Data asesmen untuk automated test."
        ),
        "status": status,
        "score": score,
    }


# GET TESTS

def test_get_existing_assessment(
    client: TestClient,
) -> None:
    _, assessment = get_latest_assessment(
        client
    )

    response = client.get(
        (
            "/api/assessments/"
            f"{assessment['id']}"
        )
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["id"] == (
        assessment["id"]
    )

    assert response_data["student_id"] == (
        assessment["student_id"]
    )

    assert response_data["score"] is not None


def test_get_nonexistent_assessment(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/assessments/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": (
            "Data asesmen tidak ditemukan."
        )
    }


# POST TESTS

def test_create_partial_draft_assessment(
    client: TestClient,
) -> None:
    student = get_not_started_student(
        client
    )

    payload = create_payload(
        student_id=student["id"],
        status="draft",
        score={
            "visual_score": 2,
            "hearing_score": 1,
            "material_preferences": [
                " Teks ",
                "Teks",
            ],
            "assistive_tools": [],
        },
    )

    response = client.post(
        "/api/assessments",
        json=payload,
    )

    assert response.status_code == 201

    response_data = response.json()

    assert (
        response_data[
            "student_assessment_status"
        ]
        == "incomplete"
    )

    assert (
        response_data[
            "analytics_invalidated"
        ]
        is False
    )

    assessment = response_data["assessment"]

    assert assessment["status"] == "draft"
    assert assessment["student_id"] == (
        student["id"]
    )

    score = assessment["score"]

    assert score is not None
    assert score["visual_score"] == 2
    assert score["hearing_score"] == 1
    assert score["communication_score"] is None

    assert score["material_preferences"] == [
        "Teks"
    ]

    detail_response = client.get(
        (
            "/api/assessments/"
            f"{assessment['id']}"
        )
    )

    assert detail_response.status_code == 200


def test_create_complete_submitted_assessment(
    client: TestClient,
) -> None:
    student = get_not_started_student(
        client
    )

    payload = create_payload(
        student_id=student["id"],
        status="submitted",
        score=complete_score_payload(),
    )

    response = client.post(
        "/api/assessments",
        json=payload,
    )

    assert response.status_code == 201

    response_data = response.json()

    assert (
        response_data[
            "student_assessment_status"
        ]
        == "complete"
    )

    assessment = response_data["assessment"]

    assert assessment["status"] == "submitted"

    score = assessment["score"]

    assert score is not None

    expected_score = complete_score_payload()

    for field_name, expected_value in (
        expected_score.items()
    ):
        assert score[field_name] == expected_value


def test_reject_submitted_assessment_with_missing_scores(
    client: TestClient,
) -> None:
    student = get_not_started_student(
        client
    )

    payload = create_payload(
        student_id=student["id"],
        status="submitted",
        score={
            "visual_score": 1,
            "hearing_score": 2,
        },
    )

    response = client.post(
        "/api/assessments",
        json=payload,
    )

    assert response.status_code == 422


def test_reject_score_outside_allowed_range(
    client: TestClient,
) -> None:
    student = get_not_started_student(
        client
    )

    payload = create_payload(
        student_id=student["id"],
        status="draft",
        score={
            "visual_score": 4,
        },
    )

    response = client.post(
        "/api/assessments",
        json=payload,
    )

    assert response.status_code == 422


def test_create_assessment_for_nonexistent_student(
    client: TestClient,
) -> None:
    payload = create_payload(
        student_id=999999,
        status="draft",
    )

    response = client.post(
        "/api/assessments",
        json=payload,
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": (
            "Data siswa tidak ditemukan."
        )
    }


def test_create_assessment_with_nonexistent_assessor(
    client: TestClient,
) -> None:
    student = get_not_started_student(
        client
    )

    payload = create_payload(
        student_id=student["id"],
        status="draft",
    )

    payload["assessor_id"] = 999999

    response = client.post(
        "/api/assessments",
        json=payload,
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": (
            "Data penilai tidak ditemukan."
        )
    }


# PATCH TESTS

def test_patch_assessment_and_invalidate_analytics(
    client: TestClient,
) -> None:
    student, assessment = (
        get_latest_assessment(client)
    )

    analytics_before = client.get(
        (
            "/api/analytics/students/"
            f"{student['id']}"
        )
    )

    assert analytics_before.status_code == 200

    response = client.patch(
        (
            "/api/assessments/"
            f"{assessment['id']}"
        ),
        json={
            "score": {
                "hearing_score": 2,
            },
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data[
            "analytics_invalidated"
        ]
        is True
    )

    assert (
        response_data[
            "student_assessment_status"
        ]
        == "complete"
    )

    assert (
        response_data["assessment"]["score"][
            "hearing_score"
        ]
        == 2
    )

    analytics_after = client.get(
        (
            "/api/analytics/students/"
            f"{student['id']}"
        )
    )

    assert analytics_after.status_code == 404


def test_patch_notes_without_invalidating_analytics(
    client: TestClient,
) -> None:
    student, assessment = (
        get_latest_assessment(client)
    )

    analytics_before = client.get(
        (
            "/api/analytics/students/"
            f"{student['id']}"
        )
    )

    assert analytics_before.status_code == 200

    response = client.patch(
        (
            "/api/assessments/"
            f"{assessment['id']}"
        ),
        json={
            "notes": (
                "Catatan administrasi diperbarui."
            ),
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data[
            "analytics_invalidated"
        ]
        is False
    )

    analytics_after = client.get(
        (
            "/api/analytics/students/"
            f"{student['id']}"
        )
    )

    assert analytics_after.status_code == 200


def test_reject_empty_patch(
    client: TestClient,
) -> None:
    _, assessment = get_latest_assessment(
        client
    )

    response = client.patch(
        (
            "/api/assessments/"
            f"{assessment['id']}"
        ),
        json={},
    )

    assert response.status_code == 422


def test_reject_incomplete_submitted_patch(
    client: TestClient,
) -> None:
    student, assessment = (
        get_latest_assessment(client)
    )

    analytics_before = client.get(
        (
            "/api/analytics/students/"
            f"{student['id']}"
        )
    )

    assert analytics_before.status_code == 200

    response = client.patch(
        (
            "/api/assessments/"
            f"{assessment['id']}"
        ),
        json={
            "score": {
                "hearing_score": None,
            },
        },
    )

    assert response.status_code == 422

    analytics_after = client.get(
        (
            "/api/analytics/students/"
            f"{student['id']}"
        )
    )

    assert analytics_after.status_code == 200


# PUT TESTS

def test_replace_assessment_with_partial_draft(
    client: TestClient,
) -> None:
    student, assessment = (
        get_latest_assessment(client)
    )

    response = client.put(
        (
            "/api/assessments/"
            f"{assessment['id']}"
        ),
        json={
            "assessment_date": (
                date.today().isoformat()
            ),
            "source_information": (
                "Observasi ulang"
            ),
            "notes": "Disimpan sebagai draft.",
            "status": "draft",
            "score": {
                "visual_score": 2,
                "material_preferences": [
                    "Visual",
                ],
                "assistive_tools": [],
            },
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data[
            "student_assessment_status"
        ]
        == "incomplete"
    )

    assert (
        response_data[
            "analytics_invalidated"
        ]
        is True
    )

    replaced_assessment = (
        response_data["assessment"]
    )

    assert replaced_assessment["status"] == (
        "draft"
    )

    assert (
        replaced_assessment["score"][
            "visual_score"
        ]
        == 2
    )

    assert (
        replaced_assessment["score"][
            "hearing_score"
        ]
        is None
    )

    analytics_response = client.get(
        (
            "/api/analytics/students/"
            f"{student['id']}"
        )
    )

    assert analytics_response.status_code == 404


def test_replace_nonexistent_assessment(
    client: TestClient,
) -> None:
    response = client.put(
        "/api/assessments/999999",
        json={
            "assessment_date": (
                date.today().isoformat()
            ),
            "status": "draft",
            "score": None,
        },
    )

    assert response.status_code == 404


# TRANSACTION SAFETY TEST

def test_database_counts_remain_unchanged(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/students/summary"
    )

    assert response.status_code == 200

    assert response.json() == {
        "total_students": 120,
        "complete": 96,
        "incomplete": 18,
        "not_started": 6,
        "total_assessments": 96,
        "total_scores": 96,
    }