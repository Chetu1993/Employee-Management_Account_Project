
def test_create_post_method(client):
    response=client.post("/employees",json={"full_name":"chetan kumar",
                                           "job_title":"backend engineer",
                                           "country":"India",
                                           "salary":100000})

    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "chetan kumar"


def test_get_employee(client,created_employee_id):
    emp_id=created_employee_id
    response=client.get(f"/employees/{emp_id}")
    data=response.json()
