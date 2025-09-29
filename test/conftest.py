# import pytest
# from app.main import app
# from app.services import auth


# @pytest.fixture()
# def override_dependencies():
#     async def fake_token_interceptor():
#         return {"id": "123", "is_admin": True}

#     def fake_verify_admin(user):
#         return True

#     app.dependency_overrides[auth.token_interceptor] = fake_token_interceptor
#     app.dependency_overrides[auth.verify_admin] = fake_verify_admin
#     app.dependency_overrides[auth.verify_owner] = fake_verify_admin
#     yield
#     app.dependency_overrides.clear()
