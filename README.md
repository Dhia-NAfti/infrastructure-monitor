# Infrastructure Monitoring API

A small Flask REST API for maintaining a server inventory and tracking infrastructure incidents. It is designed as a learning project for Python, testing, linting, Makefiles, and GitHub Actions.

## Requirements

- Python 3.10 or newer
- `make`
- Git (for version control)

## Setup

```bash
git clone <YOUR-REPOSITORY-URL>
cd infrastructure-monitor
python3 -m venv .venv
source .venv/bin/activate
make install
```

## Run the API

```bash
make run
```

The API listens on `http://127.0.0.1:5000`.

## Available endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API information |
| GET | `/health` | Health check |
| POST | `/api/servers` | Register a server |
| GET | `/api/servers` | List servers |
| GET | `/api/servers/<id>` | Get server details |
| PUT | `/api/servers/<id>/status` | Update server status |
| POST | `/api/incidents` | Create an incident |
| GET | `/api/incidents` | List incidents |
| PUT | `/api/incidents/<id>/resolve` | Resolve an incident |

## Example requests

Register a server:

```bash
curl -X POST http://127.0.0.1:5000/api/servers \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "WEB-SERVER-01",
    "ip_address": "192.168.1.10",
    "operating_system": "Ubuntu 22.04",
    "role": "Web Server"
  }'
```

List servers:

```bash
curl http://127.0.0.1:5000/api/servers
```

Update server status:

```bash
curl -X PUT http://127.0.0.1:5000/api/servers/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "UP"}'
```

## Development commands

```bash
make help
make install
make test
make lint
make ruff
make typecheck
make check
make clean
```

## CI

GitHub Actions runs Flake8, Ruff, mypy, and pytest on Python 3.10, 3.11, and 3.12 for pushes and pull requests to `main`.

## Learning notes

- Server status is updated through the API; it is not an actual ping/SSH probe.
- SQLite is used to keep the project self-contained.
- Do not put secrets or SSH private keys in source control.
- The `six` dependency is included for a separate legacy-compatibility exercise; this application targets supported modern Python versions.
