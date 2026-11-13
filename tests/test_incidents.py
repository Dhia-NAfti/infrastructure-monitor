def test_create_and_resolve_incident(client):
    server = client.post(
        "/api/servers",
        json={
            "hostname": "DB-SERVER-01",
            "ip_address": "192.168.1.20",
            "operating_system": "Ubuntu 22.04",
            "role": "Database",
        },
    ).get_json()

    response = client.post(
        "/api/incidents",
        json={
            "server_id": server["id"],
            "title": "Database service unavailable",
            "description": "The database service is not responding.",
            "severity": "CRITICAL",
        },
    )
    assert response.status_code == 201
    incident_id = response.get_json()["id"]

    resolved = client.put(f"/api/incidents/{incident_id}/resolve")
    assert resolved.status_code == 200
    assert resolved.get_json()["status"] == "RESOLVED"


def test_incident_requires_existing_server(client):
    response = client.post(
        "/api/incidents",
        json={
            "server_id": 999,
            "title": "Example",
            "description": "Example incident",
            "severity": "HIGH",
        },
    )
    assert response.status_code == 404
