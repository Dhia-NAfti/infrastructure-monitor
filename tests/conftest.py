import pytest

from app import create_app


@pytest.fixture()
def client(tmp_path):
    database = tmp_path / "test.db"
    app = create_app({
        "TESTING": True,
        "DATABASE": str(database),
    })
    with app.test_client() as test_client:
        yield test_client
