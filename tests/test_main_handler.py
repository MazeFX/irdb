import pytest

from irdb.irdb import make_app


@pytest.fixture
def app():
    return make_app()


@pytest.mark.gen_test
def test_main_handler_get(http_client, base_url):
    response = yield http_client.fetch(base_url)
    assert response.code == 200