def test_valid_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json["status"]
    assert data == "ready"

def test_invalid_enpoint(client):
    response = client.get("/abs")
    assert response.status_code == 404
    data = response.json
    assert data['error'] == "NotFound"
