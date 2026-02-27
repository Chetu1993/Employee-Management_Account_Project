from app import main
def test_employee_persisted_in_database(client):
    response=client.post("/employees",json={
        "full_name":"chetan kumar",
        "job_title":"backend_engineer",
        "country":"India",
        "salary":1000
    })

    assert response.status_code == 201
    emp_id=response.json()["employee_id"]
    # if hasattr(emp_id,"employees_db"):
    #     main.employees_db.clear()
    main.employees_db.clear()

    get_response=client.get(f"employees/{emp_id}")
    assert get_response.status_code == 200
    assert get_response.json()["full_name"] == "chetan kumar"