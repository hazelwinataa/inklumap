from fastapi.testclient import TestClient


def test_student_summary(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/students/summary"
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data == {
        "total_students": 120,
        "complete": 96,
        "incomplete": 18,
        "not_started": 6,
        "total_assessments": 96,
        "total_scores": 96,
    }


def test_get_students_default(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/students"
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["total"] == 120
    assert response_data["skip"] == 0
    assert response_data["limit"] == 20
    assert len(response_data["items"]) == 20


def test_get_students_with_limit(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/students",
        params={
            "limit": 5,
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["total"] == 120
    assert response_data["limit"] == 5
    assert len(response_data["items"]) == 5


def test_students_are_sorted_by_code(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/students",
        params={
            "limit": 10,
        },
    )

    assert response.status_code == 200

    items = response.json()["items"]

    student_codes = [
        item["student_code"]
        for item in items
    ]

    assert student_codes == sorted(
        student_codes
    )


def test_filter_complete_students(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/students",
        params={
            "status": "complete",
            "limit": 100,
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["total"] == 96

    assert all(
        item["assessment_status"]
        == "complete"
        for item in response_data["items"]
    )


def test_filter_incomplete_students(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/students",
        params={
            "status": "incomplete",
            "limit": 100,
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["total"] == 18

    assert all(
        item["assessment_status"]
        == "incomplete"
        for item in response_data["items"]
    )


def test_filter_not_started_students(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/students",
        params={
            "status": "not_started",
            "limit": 100,
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["total"] == 6

    assert all(
        item["assessment_status"]
        == "not_started"
        for item in response_data["items"]
    )


def test_search_student_by_code(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/students",
        params={
            "search": "SIS-001",
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["total"] >= 1
    assert (
        response_data["items"][0][
            "student_code"
        ]
        == "SIS-001"
    )


def test_get_existing_student_detail(
    client: TestClient,
) -> None:
    list_response = client.get(
        "/api/students",
        params={
            "search": "SIS-001",
        },
    )

    assert list_response.status_code == 200

    student_items = (
        list_response.json()["items"]
    )

    assert len(student_items) == 1

    student_id = student_items[0]["id"]

    detail_response = client.get(
        f"/api/students/{student_id}"
    )

    assert detail_response.status_code == 200

    response_data = detail_response.json()

    assert (
        response_data["student_code"]
        == "SIS-001"
    )
    assert (
        response_data["assessment_status"]
        == "complete"
    )
    assert len(
        response_data["assessments"]
    ) >= 1

    assessment = (
        response_data["assessments"][0]
    )

    assert assessment["score"] is not None

    score = assessment["score"]

    expected_score_fields = [
        "visual_score",
        "hearing_score",
        "communication_score",
        "instruction_score",
        "attention_score",
        "mobility_score",
        "assistance_score",
        "evaluation_adjustment_score",
    ]

    for field_name in expected_score_fields:
        assert field_name in score
        assert 0 <= score[field_name] <= 3


def test_get_nonexistent_student(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/students/999999"
    )

    assert response.status_code == 404

    assert response.json() == {
        "detail": (
            "Data siswa tidak ditemukan."
        )
    }


def test_invalid_student_status_filter(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/students",
        params={
            "status": "unknown",
        },
    )

    assert response.status_code == 422


def test_invalid_limit_parameter(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/students",
        params={
            "limit": 101,
        },
    )

    assert response.status_code == 422