import os

import pytest



os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key"

from app import app
from extensions import db


@pytest.fixture()
def client():

    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False
    )

    with app.app_context():
        db.drop_all()
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()