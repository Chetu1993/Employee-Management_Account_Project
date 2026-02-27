import pytest
from app import main
from fastapi.testclient import TestClient



@pytest.fixture
def client():
    with TestClient(main.app) as c:
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
    main.init_db()
    conn=main.get_connection()
    cursor=conn.cursor()
    cursor.execute('''delete from employees''')
    conn.commit()
    conn.close()
    # main.employees_db.clear()
    # main.employee_id_counter=1
