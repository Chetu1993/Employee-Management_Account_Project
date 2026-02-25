
def test_create_post_method(client):
    response=client.post("/employees",json={"full_name":"chetan kumar",
                                           "job_title":"backend engineer",
                                           "country":"India",
                                           "salary":100000})

    print(response.json())
    assert response.status_code == 201



