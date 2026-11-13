from flask import Blueprint, jsonify, request

from .database import get_db

api = Blueprint("api", __name__)


@api.get("/")
def index():
    return jsonify(
        message="Infrastructure Monitoring API",
        endpoints=["/health", "/api/servers", "/api/incidents"],
    )


@api.get("/health")
def health():
    return jsonify(status="ok", service="infrastructure-monitor")


@api.get("/api/servers")
def list_servers():
    rows = get_db().execute(
        "SELECT * FROM servers ORDER BY id"
    ).fetchall()
    return jsonify([dict(row) for row in rows])


@api.post("/api/servers")
def create_server():
    data = request.get_json(silent=True) or {}
    required = ("hostname", "ip_address", "operating_system", "role")
    missing = [field for field in required if not data.get(field)]
    if missing:
        return jsonify(error="Missing required fields", fields=missing), 400

    db = get_db()
    try:
        cursor = db.execute(
            """
            INSERT INTO servers
                (hostname, ip_address, operating_system, role)
            VALUES (?, ?, ?, ?)
            """,
            tuple(data[field] for field in required),
        )
        db.commit()
    except Exception as exc:
        db.rollback()
        if "UNIQUE constraint failed" in str(exc):
            return jsonify(error="A server with this hostname already exists"), 409
        raise

    row = db.execute(
        "SELECT * FROM servers WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    return jsonify(dict(row)), 201


@api.get("/api/servers/<int:server_id>")
def get_server(server_id):
    row = get_db().execute(
        "SELECT * FROM servers WHERE id = ?", (server_id,)
    ).fetchone()
    if row is None:
        return jsonify(error="Server not found"), 404
    return jsonify(dict(row))


@api.put("/api/servers/<int:server_id>/status")
def update_server_status(server_id):
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    allowed = {"UP", "DOWN", "MAINTENANCE", "UNKNOWN"}
    if status not in allowed:
        return jsonify(error="status must be one of: " + ", ".join(sorted(allowed))), 400

    db = get_db()
    cursor = db.execute(
        "UPDATE servers SET status = ? WHERE id = ?", (status, server_id)
    )
    db.commit()
    if cursor.rowcount == 0:
        return jsonify(error="Server not found"), 404

    row = db.execute(
        "SELECT * FROM servers WHERE id = ?", (server_id,)
    ).fetchone()
    return jsonify(dict(row))


@api.post("/api/incidents")
def create_incident():
    data = request.get_json(silent=True) or {}
    required = ("server_id", "title", "description", "severity")
    missing = [field for field in required if data.get(field) in (None, "")]
    if missing:
        return jsonify(error="Missing required fields", fields=missing), 400

    severity = str(data["severity"]).upper()
    if severity not in {"LOW", "MEDIUM", "HIGH", "CRITICAL"}:
        return jsonify(error="Invalid severity"), 400

    db = get_db()
    server = db.execute(
        "SELECT id FROM servers WHERE id = ?", (data["server_id"],)
    ).fetchone()
    if server is None:
        return jsonify(error="Server not found"), 404

    cursor = db.execute(
        """
        INSERT INTO incidents (server_id, title, description, severity)
        VALUES (?, ?, ?, ?)
        """,
        (data["server_id"], data["title"], data["description"], severity),
    )
    db.commit()
    row = db.execute(
        "SELECT * FROM incidents WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    return jsonify(dict(row)), 201


@api.get("/api/incidents")
def list_incidents():
    rows = get_db().execute(
        """
        SELECT incidents.*, servers.hostname
        FROM incidents
        JOIN servers ON servers.id = incidents.server_id
        ORDER BY incidents.id
        """
    ).fetchall()
    return jsonify([dict(row) for row in rows])


@api.put("/api/incidents/<int:incident_id>/resolve")
def resolve_incident(incident_id):
    db = get_db()
    cursor = db.execute(
        "UPDATE incidents SET status = 'RESOLVED' WHERE id = ?",
        (incident_id,),
    )
    db.commit()
    if cursor.rowcount == 0:
        return jsonify(error="Incident not found"), 404
    row = db.execute(
        "SELECT * FROM incidents WHERE id = ?", (incident_id,)
    ).fetchone()
    return jsonify(dict(row))
