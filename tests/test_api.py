from fastapi.testclient import TestClient


def test_read_spreadsheet(client: TestClient):
    response = client.get("/spreadsheet")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
