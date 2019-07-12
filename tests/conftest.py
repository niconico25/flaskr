import os
import tempfile

import pytest

from flaskr import create_app
from flaskr.db import get_db
from flaskr.db import init_db
from flaskr import models
import sqlite3

# read in SQL for populating test data
# with open(os.path.join(os.path.dirname(__file__), "data.sql"), "rb") as f:
#     _data_sql = f.read().decode("utf8")


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    # db_fd, db_path = tempfile.mkstemp(dir=os.environ['PYTHONPATH'])
    # create the app with common test config
    # app = create_app({"TESTING": True, "DATABASE": db_path})
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get('TEST_DATABASE_URL'),
    })

    # create the database and load test data
    with app.app_context():
        init_db()
        # - get_db().executescript(_data_sql)

        # INSERT INTO user (username, password)
        # VALUES
        #   ('test', 'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f'),
        #   ('other', 'pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79');
        # 
        # INSERT INTO post (title, body, author_id, created)
        # VALUES
        #   ('test title', 'test' || x'0a' || 'body', 1, '2018-01-01 00:00:00');
        db = get_db()

        test_user = models.User(
                username='test',
                password='pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f')
        other_user = models.User(
            username='other',
            password='pbkdf2:sha256:50000$kJPKsz6N$d2d4784f1b030a9761f5ccaeeaca413f27f2ecb76d6168407af962ddce849f79')
        db.session.add(test_user)
        db.session.add(other_user)
        db.session.flush()
        post = models.Post(
                title='test title',
                body='test' + '\n' + 'body',
                author_id=test_user.id,
                created='2018-01-01 00:00:00')
        db.session.add(post)
        db.session.commit()

    yield app

    # - close and remove the temporary database
    # - os.close(db_fd)
    # - os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
