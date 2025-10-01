import contextlib
from types import SimpleNamespace
from typing import Generator

import pytest
from main import app
from database import get_db_context
from services.auth import token_interceptor
from fastapi.testclient import TestClient


@pytest.fixture()
def mock_db_session():
    class DummySession:
        def __getattr__(self, name):
            # Return a callable no-op for any unexpected method access
            def _noop(*args, **kwargs):
                return None

            return _noop

        def close(self):
            return None

    yield DummySession()


def _override_get_db_context(mock_db_session) -> Generator:
    yield mock_db_session


def _override_token_interceptor() -> SimpleNamespace:
    # Admin user to pass verify_admin/verify_owner checks
    return SimpleNamespace(
        id="11111111-1111-1111-1111-111111111111",
        username="admin",
        first_name="Admin",
        last_name="User",
        is_admin=True,
    )


@pytest.fixture(autouse=True)
def override_dependencies(mock_db_session):
    # Apply overrides before each test
    app.dependency_overrides[get_db_context] = lambda: _override_get_db_context(
        mock_db_session
    )
    app.dependency_overrides[token_interceptor] = _override_token_interceptor

    yield

    # Cleanup overrides after each test
    with contextlib.suppress(Exception):
        app.dependency_overrides.pop(get_db_context, None)
        app.dependency_overrides.pop(token_interceptor, None)


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
