from unittest.mock import AsyncMock, MagicMock

import pytest
from app.database import get_db_context
from app.main import app
from app.services.auth import token_interceptor
from fastapi.testclient import TestClient

client = TestClient(app)


def mock_token_interceptor(token: str = ""):
    return {"is_admin": True}


app.dependency_overrides[token_interceptor] = mock_token_interceptor
app.dependency_overrides[get_db_context] = AsyncMock()


@pytest.mark.asyncio
async def test_create_user(mocker):
    body = {
        "username": "user 1",
        "email": "email1@gmail.com",
        "first_name": "user 1",
        "last_name": "user 1",
        "password": "Password1",
        "company_id": "23a2ac73-a8a5-4adc-8703-0702cd5367e9",
    }

    mocker.patch("services.auth.verify_admin", return_value=True)
    mocker.patch(
        "services.user.create_user",
        return_value=body,
    )

    response = client.post("/users/", json=body)

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == body["username"]
    assert data["email"] == body["email"]


@pytest.mark.asyncio
async def test_get_users(mocker):
    mocker.patch("services.auth.verify_admin", return_value=True)
    mocker.patch(
        "services.user.get_users", return_value=[{"id": "1", "username": "testuser"}]
    )

    response = client.get("/users/?page=1&limit=10")

    assert response.status_code == 200
    assert response.json()[0]["username"] == "testuser"


@pytest.mark.asyncio
async def test_get_user_by_id(mocker):
    mocker.patch("services.auth.verify_owner", return_value=True)
    mocker.patch(
        "services.user.get_user_by_id", return_value={"id": "1", "username": "testuser"}
    )

    response = client.get("/users/1")

    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


@pytest.mark.asyncio
async def test_update_user(mocker):
    body = {
        "first_name": "user 1",
        "last_name": "user 1",
    }

    mocker.patch("services.auth.verify_owner", return_value=True)
    mocker.patch(
        "services.user.update_user",
        return_value=body,
    )

    response = client.put("/users/1", json=body)

    assert response.status_code == 200
    assert response.json()["first_name"] == body["first_name"]


@pytest.mark.asyncio
async def test_delete_user(mocker):
    mocker.patch("services.auth.verify_owner", return_value=True)
    mocker.patch("services.user.delete_user", return_value=True)

    response = client.delete("/users/1")

    assert response.status_code == 204
    assert response.json() == "Ok"
