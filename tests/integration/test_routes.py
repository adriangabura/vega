def test_read_users(fastapi_test_client):
    client = fastapi_test_client
    response = client.get("/users/")