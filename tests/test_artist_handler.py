import pytest
import json
import tornado


@pytest.fixture
def artists_base_url(base_url):
    return base_url + '/artists'


@pytest.mark.gen_test
def test_artist_handler_get(http_client, artists_base_url):
    artist = {"Id": 760, "Name": "\"Weird Al\" Yankovic"}

    response = yield http_client.fetch(artists_base_url)
    assert response.code == 200

    json_result = json.loads(response.body)
    assert json_result == artist


@pytest.mark.gen_test
def test_artists_handler_create_new_post_fails_malformed_data(http_client, artists_base_url):
    test_data = {"Named": "Rock Stars"}

    body = json.dumps(test_data)
    with pytest.raises(tornado.httpclient.HTTPClientError):
        response = yield http_client.fetch(artists_base_url, method="POST", body=body)


@pytest.mark.gen_test
def test_artists_handler_create_new_post(http_client, artists_base_url):
    test_data = {"Name": "Rock Stars"}

    body = json.dumps(test_data)
    response = yield http_client.fetch(artists_base_url, method="POST", body=body)

    assert response.code == 201
    assert response.body == b'{}'

# @pytest.mark.gen_test
# def test_artists_handler_put(http_client, base_url):
#     test_data = {"Rock": "Stars"}
#
#     body = urllib.parse.urlencode(test_data)
#
#     with pytest.raises(tornado.httpclient.HTTPClientError):
#         response = yield http_client.fetch(base_url, method="PUT", body=body)
#
#
# @pytest.mark.gen_test
# def test_artists_handler_delete(http_client, base_url):
#     with pytest.raises(tornado.httpclient.HTTPClientError):
#         response = yield http_client.fetch(base_url, method="DELETE")

