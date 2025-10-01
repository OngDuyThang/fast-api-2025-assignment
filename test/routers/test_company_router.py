from uuid import uuid4

import routers.company as company_router
from common.enums import CompanyMode
from models.company import CompanyDto


def _fake_company_dto(company_id=None):
    cid = str(company_id or uuid4())
    return {
        "id": cid,
        "name": f"Company {cid[:8]}",
        "description": f"Description {cid[:8]}",
        "mode": CompanyMode.OUTSOURCE,
        "rating": 4.5,
        "created_at": None,
        "updated_at": None,
    }


def test_create_company_success(client, monkeypatch):
    payload = {
        "name": "Company Name",
        "description": "Company Description",
        "mode": "outsource",
        "rating": 4.5,
    }
    expected = _fake_company_dto()

    def _mock_create_company(request, db):
        return expected

    monkeypatch.setattr(
        company_router.company_service, "create_company", _mock_create_company
    )

    res = client.post(
        "/companies/",
        json=payload,
        headers={"Authorization": "Bearer test"},
    )
    assert res.status_code == 201
    assert res.json()["id"] == expected["id"]


def test_get_companies_success(client, monkeypatch):
    expected = [_fake_company_dto(), _fake_company_dto()]

    def _mock_get_companies(page, limit, db):
        return expected

    monkeypatch.setattr(
        company_router.company_service, "get_companies", _mock_get_companies
    )

    res = client.get(
        "/companies/?page=1&limit=2", headers={"Authorization": "Bearer test"}
    )
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) == 2


def test_get_company_by_id_success(client, monkeypatch):
    company_id = str(uuid4())
    expected = _fake_company_dto(company_id)

    def _mock_get_company_by_id(cid, user, db):
        return expected

    monkeypatch.setattr(
        company_router.company_service, "get_company_by_id", _mock_get_company_by_id
    )

    res = client.get(
        f"/companies/{company_id}", headers={"Authorization": "Bearer test"}
    )
    assert res.status_code == 200
    assert res.json()["id"] == company_id


def test_update_company_success(client, monkeypatch):
    company_id = str(uuid4())
    payload = {"description": "New description", "mode": "outsource"}
    base = _fake_company_dto(company_id)
    expected = {**base, **payload}

    def _mock_update_company(cid, request, db):
        return expected

    monkeypatch.setattr(
        company_router.company_service, "update_company", _mock_update_company
    )

    res = client.put(
        f"/companies/{company_id}",
        json=payload,
        headers={"Authorization": "Bearer test"},
    )
    print(res.text)
    assert res.status_code == 200
    assert res.json()["description"] == "New description"


def test_delete_company_success(client, monkeypatch):
    company_id = str(uuid4())

    def _mock_delete_company(cid, db):
        return "Ok"

    monkeypatch.setattr(
        company_router.company_service, "delete_company", _mock_delete_company
    )

    res = client.delete(
        f"/companies/{company_id}", headers={"Authorization": "Bearer test"}
    )
    assert res.status_code == 200
    assert res.json() == "Ok"
