def test_salary_must_be_positive(client):
    response=client.post("/employees",json={
        "full_name":"chetan kumar",
        "job_title":"Tester",
        "country":"India",
        "salary":-20000
    })

    assert response.status_code == 400