import routers.auth as auth_router


def test_login_success(client, monkeypatch):
    def _mock_authenticate_user(username, password, db):
        return {"id": "u1", "username": username}

    def _mock_create_access_token(user, expires):
        return "fake.jwt.token"

    monkeypatch.setattr(auth_router, "authenticate_user", _mock_authenticate_user)
    monkeypatch.setattr(auth_router, "create_access_token", _mock_create_access_token)

    res = client.post(
        "/auth/login",
        data={"username": "jdoe", "password": "Password1"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert res.status_code == 201
    body = res.json()
    assert body["access_token"] == "fake.jwt.token"
    assert body["token_type"] == "bearer"
