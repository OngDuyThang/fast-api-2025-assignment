from uuid import uuid4

import pytest
import routers.user as user_router


def _fake_user_dto(user_id=None):
    uid = str(user_id or uuid4())
    return {
        "id": uid,
        "username": f"user_{uid[:8]}",
        "email": "u@example.com",
        "first_name": "U",
        "last_name": "Ser",
        "company_id": None,
        "tasks": [],
        "created_at": None,
        "updated_at": None,
    }


def test_create_user_success(client, monkeypatch):
    payload = {
        "username": "jdoe",
        "email": "j@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "Password1",
    }

    expected = _fake_user_dto()

    def _mock_create_user(request, db):
        return expected

    monkeypatch.setattr(user_router.user_service, "create_user", _mock_create_user)

    res = client.post("/users/", json=payload)
    assert res.status_code == 201
    assert res.json()["id"] == expected["id"]


def test_get_users_success(client, monkeypatch):
    expected = [_fake_user_dto(), _fake_user_dto()]

    def _mock_get_users(page, limit, db):
        return expected

    monkeypatch.setattr(user_router.user_service, "get_users", _mock_get_users)

    res = client.get("/users/?page=1&limit=2")
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) == 2


def test_get_user_by_id_success(client, monkeypatch):
    user_id = str(uuid4())
    expected = _fake_user_dto(user_id)

    def _mock_get_user_by_id(uid, db):
        assert uid == user_id
        return expected

    monkeypatch.setattr(
        user_router.user_service, "get_user_by_id", _mock_get_user_by_id
    )

    res = client.get(f"/users/{user_id}")
    assert res.status_code == 200
    assert res.json()["id"] == user_id


def test_update_user_success(client, monkeypatch):
    user_id = str(uuid4())
    payload = {"first_name": "New", "last_name": "Name"}
    expected = {**_fake_user_dto(user_id), **payload}

    def _mock_update_user(uid, request, db):
        assert uid == user_id
        return expected

    monkeypatch.setattr(user_router.user_service, "update_user", _mock_update_user)

    res = client.put(f"/users/{user_id}", json=payload)
    assert res.status_code == 200
    body = res.json()
    assert body["id"] == user_id
    assert body["first_name"] == "New"
    assert body["last_name"] == "Name"


def test_delete_user_success(client, monkeypatch):
    user_id = str(uuid4())

    def _mock_delete_user(uid, db):
        assert uid == user_id
        return "Ok"

    monkeypatch.setattr(user_router.user_service, "delete_user", _mock_delete_user)

    res = client.delete(f"/users/{user_id}")
    assert res.status_code == 200
    assert res.json() == "Ok"
