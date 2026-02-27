
def test_create_post_method(client):
    response=client.post("/employees",json={"full_name":"chetan kumar",
                                           "job_title":"backend engineer",
                                           "country":"India",
                                           "salary":100000})

    print(response.json())
    assert response.status_code == 201
    data = response.json()
    assert data["full_name"] == "chetan kumar"
    emp_id=data["employee_id"]
    update_response = client.put(f"/employees/{emp_id}", json={"full_name": "chetan",
                                                               "job_title": "frontend engineer",
                                                               "country": "India",
                                                               "salary": 50000})

    assert update_response.status_code == 200
    data = update_response.json()
    assert data["full_name"] == "chetan"
    assert data["job_title"] == "frontend engineer"
    assert data["country"] == "India"



def test_get_employee(client,created_employee_id):
    emp_id=created_employee_id
    response=client.get(f"/employees/{emp_id}")
    data=response.json()
    assert data["employee_id"]==emp_id
    assert data["full_name"] == "chetan kumar"

def test_delete_employee(client):
    create_response = client.post("/employees", json={"full_name": "chetan kumar",
                                               "job_title": "backend engineer",
                                               "country": "India",
                                               "salary": 100000})

    assert create_response.status_code == 201
    emp_id=create_response.json()["employee_id"]
    delete_response = client.delete(f"/employees/{emp_id}")
    assert delete_response.status_code == 204
    get_response=client.get(f"/employees/{emp_id}")
    assert get_response.status_code == 204