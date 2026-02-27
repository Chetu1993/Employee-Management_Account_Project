def test_salary_metrics_by_country(client):
    client.post("/employees",json={"full_name":"A",
                                   "job_title":"Engineer",
                                   "country":"India",
                                   "salary":100000})

    client.post("/employees", json={"full_name": "B",
                                    "job_title": "Engineer",
                                    "country": "India",
                                    "salary": 200000})

    response=client.get("/metrics/salary?country=India")

    assert response.status_code == 200
    data=response.json()
    assert data["min_salary"] == 100000
    assert data["max_salary"] == 200000
    assert data["average_salary"] == 150000.0


def test_salary_metrics_by_job_title(client):
    client.post("/employees", json={
        "full_name": "A",
        "job_title": "Tester",
        "country": "India",
        "salary": 50000
    })

    client.post("/employees", json={
        "full_name": "B",
        "job_title": "Tester",
        "country": "US",
        "salary": 70000
    })

    response = client.get("/metrics/salary?job_title=Tester")

    assert response.status_code == 200
    data = response.json()

    assert data["average_salary"] == 60000

def test_metrics_salary_no_data(client):
    response=client.get("/metrics/salary?country=Germany")
    assert response.status_code == 404