import pytest
import urllib
import tornado

from irdb.irdb import make_app


@pytest.fixture
def app():
    return make_app()


@pytest.mark.gen_test
def test_main_handler_get(http_client, base_url):
    with pytest.raises(tornado.httpclient.HTTPClientError):
        response = yield http_client.fetch(base_url, follow_redirects=False)

        assert response.code == 302

@pytest.mark.gen_test
def test_main_handler_post(http_client, base_url):
    test_data = {"Rock": "Stars"}

    body = urllib.parse.urlencode(test_data)

    with pytest.raises(tornado.httpclient.HTTPClientError):
        response = yield http_client.fetch(base_url, method="POST", body=body)

        assert response.code == 403

@pytest.mark.gen_test
def test_main_handler_put(http_client, base_url):
    test_data = {"Rock": "Stars"}

    body = urllib.parse.urlencode(test_data)

    with pytest.raises(tornado.httpclient.HTTPClientError):
        response = yield http_client.fetch(base_url, method="PUT", body=body)

        assert response.code == 403

@pytest.mark.gen_test
def test_main_handler_delete(http_client, base_url):
    # test_data = {"Rock": "Stars"}
    #
    # body = urllib.parse.urlencode(test_data)
    with pytest.raises(tornado.httpclient.HTTPClientError):
        response = yield http_client.fetch(base_url, method="DELETE")

        assert response.code == 403
