import pytest
import json
import tornado


@pytest.fixture
def songs_base_url(base_url):
    return base_url + '/songs'


@pytest.mark.gen_test
def test_song_handler_get(http_client, songs_base_url):
    song = {"Id": 190,
            "Name": "(Don't Fear) The Reaper",
            "Year": 1975,
            "Artist": "Blue Öyster Cult",
            "Shortname": "dontfearthereaper",
            "Bpm": 141,
            "Duration": 322822,
            "Genre": "Classic Rock",
            "SpotifyId": "5QTxFnGygVM4jFQiBovmRo",
            "Album": "Agents of Fortune"
            }

    response = yield http_client.fetch(songs_base_url)
    assert response.code == 200

    json_result = json.loads(response.body)
    assert json_result == song


@pytest.mark.gen_test
def test_songs_handler_create_new_post_fails_malformed_data(http_client, songs_base_url):
    test_data = {"Named": "Rock Stars"}

    body = json.dumps(test_data)
    with pytest.raises(tornado.httpclient.HTTPClientError):
        response = yield http_client.fetch(songs_base_url, method="POST", body=body)


@pytest.mark.gen_test
def test_songs_handler_create_new_post(http_client, songs_base_url):
    test_data = {"Name": "Back In The Game",
                 "Year": 2013,
                 "Artist": "Airbourne",
                 "Shortname": "backinthegame",
                 "Bpm": 141,
                 "Duration": 322822,
                 "Genre": "Classic Rock",
                 "SpotifyId": "5QTxFnGygVM4jFQiBovmRo",
                 "Album": "Black Dog Barking"
                 }

    body = json.dumps(test_data)
    response = yield http_client.fetch(songs_base_url, method="POST", body=body)

    assert response.code == 201
    assert response.body == b'{}'
