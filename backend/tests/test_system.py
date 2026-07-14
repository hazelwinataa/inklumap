from fastapi.testclient import TestClient


def test_root_endpoint(
    client: TestClient,
) -> None:
    response = client.get("/")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["application"] == "InkluMap"
    assert response_data["version"] == "0.3.0"


def test_health_endpoint(
    client: TestClient,
) -> None:
    response = client.get("/health")

    assert response.status_code == 200

    response_data = response.json()

    assert response_data == {
        "status": "healthy",
        "service": "InkluMap API",
    }


def test_database_health_endpoint(
    client: TestClient,
) -> None:
    response = client.get(
        "/health/database"
    )

    assert response.status_code == 200

    response_data = response.json()

    assert response_data["status"] == "healthy"
    assert response_data["service"] == "PostgreSQL"
    assert (
        response_data["database_user"]
        == "inklumap_user"
    )
    assert (
        response_data["database_name"]
        == "inklumap_db"
    )