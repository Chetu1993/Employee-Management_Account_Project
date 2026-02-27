def test_salary_must_be_positive(client):
    response=client.post("/employees",json={
        "full_name":"chetan kumar",
        "job_title":"Tester",
        "country":"India",
        "salary":-20000
    })

    assert response.status_code == 422


def test_salary_cannot_decrease_on_update(client):
    create_response=client.post("/employees",json={
        "full_name":"chetan kumar",
        "job_title":"Tester",
        "country":"India",
        "salary":50000
    })
    employee_id=create_response.json()["employee_id"]
    update_response = client.put(f"/employees/{employee_id}",json={
        "full_name":"chetan kumar",
        "job_title":"Tester",
        "country":"India",
        "salary":30000
    })

    assert update_response.status_code == 400

def test_salary_calculation_for_india(client,created_employee_id):
    response=client.get(f"/employees/{created_employee_id}/salary")
    assert response.status_code == 200
    data=response.json()
    assert data["gross_salary"] == 100000
    assert data["deduction"] == 10000
    assert data["net_salary"] ==90000