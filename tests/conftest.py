import pytest

from irdb.irdb import make_app


@pytest.fixture
def app():
    return make_app()