import pytest

from app import main
from fastapi.testclient import TestClient

from app.main import app,employees_db


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def created_employee_id(client):
    # Create employee
    response = client.post("/employees", json={
        "full_name": "chetan kumar",
        "job_title": "backend engineer",
        "country": "India",
        "salary": 100000
    })
    assert response.status_code == 201
    data = response.json()
    return data["employee_id"]

@pytest.fixture(autouse=True)
def reset_employees():
    main.employees_db.clear()
    main.employee_id_counter=1
