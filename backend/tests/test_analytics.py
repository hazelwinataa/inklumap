import pytest
from fastapi.testclient import TestClient


MODEL_VERSION = "hierarchical_gower_v1"


def test_analytics_summary(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/summary"
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["model_version"]
        == MODEL_VERSION
    )
    assert (
        response_data["model_name"]
        == "hierarchical_gower"
    )
    assert response_data[
        "silhouette_score"
    ] == pytest.approx(
        0.6757311738403144
    )

    assert response_data["total_students"] == 96
    assert response_data["cluster_count"] == 5

    assert response_data["high_priority"] == 16
    assert response_data["medium_priority"] == 73
    assert response_data["low_priority"] == 7

    assert response_data["critical_access"] == 40
    assert response_data[
        "dbscan_unique_cases"
    ] == 4
    assert response_data[
        "needs_human_review"
    ] == 58


def test_analytics_summary_unknown_model(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/summary",
        params={
            "model_version": "unknown_model",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": (
            "Data analytics untuk model "
            "tersebut tidak ditemukan."
        )
    }


def test_get_cluster_profiles(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/clusters"
    )

    assert response.status_code == 200

    response_data = response.json()

    assert isinstance(response_data, list)
    assert len(response_data) == 5

    cluster_numbers = [
        cluster["cluster_number"]
        for cluster in response_data
    ]

    assert cluster_numbers == [1, 2, 3, 4, 5]

    cluster_sizes = [
        cluster["cluster_size"]
        for cluster in response_data
    ]

    assert sum(cluster_sizes) == 96

    for cluster in response_data:
        assert (
            cluster["model_version"]
            == MODEL_VERSION
        )
        assert (
            cluster["distance_metric"]
            == "gower"
        )
        assert cluster["linkage"] == "average"
        assert cluster["cluster_name"]
        assert cluster["dominant_need"]
        assert cluster["description"]

        assert isinstance(
            cluster["recommendations"],
            list,
        )
        assert len(
            cluster["recommendations"]
        ) > 0

        assert cluster[
            "medoid_student_code"
        ].startswith("SIS-")


def test_get_analytics_students_default(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/students"
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["total"] == 96
    assert response_data["skip"] == 0
    assert response_data["limit"] == 20
    assert len(response_data["items"]) == 20


def test_analytics_students_limit_and_sorting(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/students",
        params={
            "limit": 5,
        },
    )

    assert response.status_code == 200

    response_data = response.json()
    items = response_data["items"]

    assert len(items) == 5

    student_codes = [
        item["student_code"]
        for item in items
    ]

    assert student_codes == sorted(
        student_codes
    )


def test_filter_high_priority_students(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/students",
        params={
            "priority_level": "high",
            "limit": 100,
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["total"] == 16
    assert len(response_data["items"]) == 16

    assert all(
        item["priority_level"] == "high"
        for item in response_data["items"]
    )


def test_filter_critical_access_students(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/students",
        params={
            "critical_access": True,
            "limit": 100,
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["total"] == 40

    assert all(
        item["critical_access_flag"]
        is True
        for item in response_data["items"]
    )


def test_filter_students_needing_review(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/students",
        params={
            "needs_review": True,
            "limit": 100,
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["total"] == 58

    assert all(
        item["needs_human_review"]
        is True
        for item in response_data["items"]
    )


def test_filter_students_by_cluster(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/students",
        params={
            "cluster_number": 2,
            "limit": 100,
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["total"] == 22

    assert all(
        item["cluster_number"] == 2
        for item in response_data["items"]
    )


def test_search_analytics_student_by_code(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/students",
        params={
            "search": "SIS-001",
        },
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["total"] >= 1

    student_codes = [
        item["student_code"]
        for item in response_data["items"]
    ]

    assert "SIS-001" in student_codes


def test_get_existing_analytics_student_detail(
    client: TestClient,
) -> None:
    list_response = client.get(
        "/api/analytics/students",
        params={
            "limit": 1,
        },
    )

    assert list_response.status_code == 200

    first_student = (
        list_response.json()["items"][0]
    )

    student_id = first_student["student_id"]

    response = client.get(
        (
            "/api/analytics/students/"
            f"{student_id}"
        )
    )

    assert response.status_code == 200

    response_data = response.json()

    assert (
        response_data["student_id"]
        == student_id
    )
    assert (
        response_data["student_code"]
        == first_student["student_code"]
    )
    assert (
        response_data["model_version"]
        == MODEL_VERSION
    )

    assert isinstance(
        response_data["dominant_needs"],
        list,
    )
    assert isinstance(
        response_data[
            "critical_access_domains"
        ],
        list,
    )
    assert isinstance(
        response_data[
            "cluster_recommendations"
        ],
        list,
    )
    assert isinstance(
        response_data[
            "individual_recommendations"
        ],
        list,
    )

    assert response_data["cluster_name"]
    assert response_data["priority_level"]
    assert response_data[
        "recommendation_status"
    ] == "generated"


def test_get_nonexistent_analytics_student(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/students/999999"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": (
            "Hasil analytics siswa "
            "tidak ditemukan."
        )
    }


def test_invalid_priority_level_filter(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/students",
        params={
            "priority_level": "urgent",
        },
    )

    assert response.status_code == 422


def test_invalid_analytics_limit(
    client: TestClient,
) -> None:
    response = client.get(
        "/api/analytics/students",
        params={
            "limit": 0,
        },
    )

    assert response.status_code == 422