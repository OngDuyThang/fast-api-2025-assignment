from types import SimpleNamespace
from uuid import uuid4

import pytest
from fastapi import HTTPException

import services.user as user_service


class DummyUser:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)


class _AttrComparable:
    def __eq__(self, other):
        # Return True for simplicity; our FakeQuery controls the actual result
        return True


class UserStub:
    # Class attributes used in service filter expression
    username = _AttrComparable()
    email = _AttrComparable()

    def __init__(self, **kwargs):
        # Behave like ORM model instance for constructed user
        for k, v in kwargs.items():
            setattr(self, k, v)
        # Ensure fields required by UserDto exist
        self.id = getattr(self, "id", uuid4())
        self.tasks = getattr(self, "tasks", [])
        self.company_id = getattr(self, "company_id", None)


class FakeQuery:
    def __init__(self, result=None, all_result=None):
        self._first = result
        self._all = all_result
        self._filters = []

    def filter(self, *args, **kwargs):
        self._filters.append((args, kwargs))
        return self

    def options(self, *args, **kwargs):
        return self

    def order_by(self, *args, **kwargs):
        return self

    def offset(self, *args, **kwargs):
        return self

    def limit(self, *args, **kwargs):
        return self

    def first(self):
        return self._first

    def all(self):
        return self._all


class FakeSession:
    def __init__(self, query_map=None):
        # query_map: { model_symbol: FakeQuery }
        self.query_map = query_map or {}
        self.added = []
        self.deleted = []
        self.committed = False
        self.refreshed = []

    def query(self, model):
        return self.query_map.get(model, FakeQuery())

    def add(self, instance):
        self.added.append(instance)

    def commit(self):
        self.committed = True

    def refresh(self, instance):
        # Simulate DB-populated fields after commit
        if not hasattr(instance, "id") or instance.id is None:
            instance.id = uuid4()
        if not hasattr(instance, "tasks"):
            instance.tasks = []
        self.refreshed.append(instance)

    def delete(self, instance):
        self.deleted.append(instance)


def _mk_request_create(**overrides):
    req = {
        "username": "jdoe",
        "email": "j@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "Password1",
        "company_id": None,
        "created_at": None,
        "updated_at": None,
    }
    req.update(overrides)
    return SimpleNamespace(**req)


def _mk_request_update(**overrides):
    req = {"first_name": "New", "last_name": "Name"}
    req.update(overrides)
    return SimpleNamespace(**req)


def _user_kwargs(**overrides):
    base = {
        "id": uuid4(),
        "username": "jdoe",
        "email": "j@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "password": "HASHED",
        "company_id": None,
        "is_admin": False,
        "tasks": [],
        "created_at": None,
        "updated_at": None,
    }
    base.update(overrides)
    return base


def test_create_user_success(monkeypatch):
    # Arrange
    req = _mk_request_create()

    # No existing user
    query_for_uniqueness = FakeQuery(result=None)

    session = FakeSession(query_map={None: FakeQuery()})

    def _fake_query(model):
        # uniqueness query is for user_service.User; accept either the real or our stub
        if model is user_service.User or model is UserStub:
            return query_for_uniqueness
        return FakeQuery()

    session.query = _fake_query

    def _fake_hashed(_password):
        return "HASHED"

    monkeypatch.setattr(user_service, "create_hashed_password", _fake_hashed)
    # Monkeypatch the ORM model symbol to our stub class (not a function)
    monkeypatch.setattr(user_service, "User", UserStub)

    # Act
    result = user_service.create_user(req, session)

    # Assert
    assert getattr(result, "username") == req.username
    assert result.email == req.email
    assert hasattr(session, "committed") and session.committed is True


def test_create_user_duplicate(monkeypatch):
    req = _mk_request_create()
    # Existing user found
    existing = DummyUser(**_user_kwargs())
    session = FakeSession()

    def _fake_query(model):
        return FakeQuery(result=existing)

    session.query = _fake_query
    # also ensure any constructor substitution still returns a user-like object
    monkeypatch.setattr(user_service, "create_hashed_password", lambda p: "HASHED")
    monkeypatch.setattr(user_service, "User", UserStub)

    with pytest.raises(HTTPException) as exc:
        user_service.create_user(req, session)
    assert exc.value.status_code == 400


def test_get_users_success(monkeypatch):
    users = [DummyUser(**_user_kwargs()), DummyUser(**_user_kwargs())]
    session = FakeSession()

    def _fake_query(model):
        return FakeQuery(all_result=users)

    session.query = _fake_query

    result = user_service.get_users(page=1, limit=2, db=session)
    assert isinstance(result, list)
    assert len(result) == 2


def test_get_user_by_id_found(monkeypatch):
    user = DummyUser(**_user_kwargs())
    session = FakeSession()

    def _fake_query(model):
        return FakeQuery(result=user)

    session.query = _fake_query

    result = user_service.get_user_by_id(str(user.id), session)
    assert result.id == user.id


def test_get_user_by_id_not_found():
    session = FakeSession()

    def _fake_query(model):
        return FakeQuery(result=None)

    session.query = _fake_query

    with pytest.raises(HTTPException) as exc:
        user_service.get_user_by_id(str(uuid4()), session)
    assert exc.value.status_code == 404


def test_update_user_success():
    user = DummyUser(**_user_kwargs(first_name="Old", last_name="Old"))
    session = FakeSession()

    def _fake_query(model):
        return FakeQuery(result=user)

    session.query = _fake_query

    req = _mk_request_update(first_name="New", last_name="Name")
    result = user_service.update_user(str(user.id), req, session)
    assert result.first_name == "New"
    assert result.last_name == "Name"
    assert session.committed is True


def test_update_user_not_found():
    session = FakeSession()

    def _fake_query(model):
        return FakeQuery(result=None)

    session.query = _fake_query

    with pytest.raises(HTTPException) as exc:
        user_service.update_user(str(uuid4()), _mk_request_update(), session)
    assert exc.value.status_code == 404


def test_delete_user_success():
    user = DummyUser(**_user_kwargs())
    session = FakeSession()

    def _fake_query(model):
        return FakeQuery(result=user)

    session.query = _fake_query

    result = user_service.delete_user(str(user.id), session)
    assert result == "Ok"
    assert user in session.deleted
    assert session.committed is True


def test_delete_user_not_found():
    session = FakeSession()

    def _fake_query(model):
        return FakeQuery(result=None)

    session.query = _fake_query

    with pytest.raises(HTTPException) as exc:
        user_service.delete_user(str(uuid4()), session)
    assert exc.value.status_code == 404
