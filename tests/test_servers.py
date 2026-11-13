def server_payload():
    return {
        "hostname": "WEB-SERVER-01",
        "ip_address": "192.168.1.10",
        "operating_system": "Ubuntu 22.04",
        "role": "Web Server",
    }


def test_create_and_list_server(client):
    response = client.post("/api/servers", json=server_payload())
    assert response.status_code == 201
    assert response.get_json()["status"] == "UNKNOWN"

    listing = client.get("/api/servers")
    assert listing.status_code == 200
    assert len(listing.get_json()) == 1


def test_create_server_requires_fields(client):
    response = client.post("/api/servers", json={"hostname": "INCOMPLETE"})
    assert response.status_code == 400


def test_duplicate_hostname_returns_conflict(client):
    client.post("/api/servers", json=server_payload())
    response = client.post("/api/servers", json=server_payload())
    assert response.status_code == 409


def test_update_server_status(client):
    created = client.post("/api/servers", json=server_payload()).get_json()
    response = client.put(
        f"/api/servers/{created['id']}/status",
        json={"status": "UP"},
    )
    assert response.status_code == 200
    assert response.get_json()["status"] == "UP"


def test_missing_server_returns_404(client):
    response = client.get("/api/servers/999")
    assert response.status_code == 404
