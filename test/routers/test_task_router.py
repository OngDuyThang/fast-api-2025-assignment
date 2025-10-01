from uuid import uuid4

import routers.task as task_router
from common.enums import TaskPriority, TaskStatus
from models.task import TaskDto


def _fake_task_dto(task_id=None):
    tid = str(task_id or uuid4())
    return {
        "id": tid,
        "summary": f"Summary {tid[:8]}",
        "description": f"Description {tid[:8]}",
        "status": TaskStatus.BACKLOG,
        "priority": TaskPriority.LOW,
        "owner_id": None,
        "created_at": None,
        "updated_at": None,
    }


def test_create_task_success(client, monkeypatch):
    payload = {
        "summary": "Task summary",
        "description": "Task description",
        "status": "backlog",
        "priority": "low",
    }
    expected = _fake_task_dto()

    def _mock_create_task(request, user, db):
        return expected

    monkeypatch.setattr(task_router.task_service, "create_task", _mock_create_task)

    res = client.post(
        "/tasks/",
        json=payload,
        headers={"Authorization": "Bearer test"},
    )
    assert res.status_code == 201
    assert res.json()["id"] == expected["id"]


def test_get_tasks_success(client, monkeypatch):
    expected = [_fake_task_dto(), _fake_task_dto()]

    def _mock_get_tasks(page, limit, user, db):
        return expected

    monkeypatch.setattr(task_router.task_service, "get_tasks", _mock_get_tasks)

    res = client.get("/tasks/?page=1&limit=2", headers={"Authorization": "Bearer test"})
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) == 2


def test_get_task_by_id_success(client, monkeypatch):
    task_id = str(uuid4())
    expected = _fake_task_dto(task_id)

    def _mock_get_task_by_id(tid, user, db):
        return expected

    monkeypatch.setattr(
        task_router.task_service, "get_task_by_id", _mock_get_task_by_id
    )

    res = client.get(f"/tasks/{task_id}", headers={"Authorization": "Bearer test"})
    assert res.status_code == 200
    assert res.json()["id"] == task_id


def test_update_task_success(client, monkeypatch):
    task_id = str(uuid4())
    payload = {
        "summary": "New summary",
        "description": "New description",
        "status": "todo",
        "priority": "medium",
    }
    base = _fake_task_dto(task_id)
    expected = TaskDto(
        **{
            **base,
            **{
                "summary": payload["summary"],
                "description": payload["description"],
                "status": TaskStatus.TODO,
                "priority": TaskPriority.MEDIUM,
            },
        }
    )

    def _mock_update_task(tid, request, user, db):
        return expected

    monkeypatch.setattr(task_router.task_service, "update_task", _mock_update_task)

    res = client.put(
        f"/tasks/{task_id}",
        json=payload,
        headers={"Authorization": "Bearer test"},
    )
    assert res.status_code == 200
    assert res.json()["summary"] == "New summary"


def test_delete_task_success(client, monkeypatch):
    task_id = str(uuid4())

    def _mock_delete_task(tid, user, db):
        return "Ok"

    monkeypatch.setattr(task_router.task_service, "delete_task", _mock_delete_task)

    res = client.delete(f"/tasks/{task_id}", headers={"Authorization": "Bearer test"})
    assert res.status_code == 200
    assert res.json() == "Ok"
