
def test_create_post_method(client):
    response=client.post("/employees",json={"full_name":"chetan kumar",
                                           "job_title":"backend engineer",
                                           "country":"India",
                                           "salary":100000})

    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "chetan kumar"


def test_get_employee(client):
    emp_id="some_id"
    response=client.get(f"/employees")
    data=response.json()
    assert data["employee_id"]==emp_id
    assert data["full_name"] == "chetan kumar"
