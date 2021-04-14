# -*- coding: utf-8 -*-
"""Handlers Collection.

Module containing all the used Request Handlers for the Tornado Server.
"""


import json

from tornado.web import RequestHandler
from .schemas import ArtistSchema, SongSchema


class BaseHandler(RequestHandler):

    async def json_response(self, data, status_code=200):
        self.set_status(status_code)
        self.set_header("Content-Type", 'application/json')

        data = await self._json_serialize(data)
        self.write(data)

    async def action_not_allowed(self):
        await self.json_response({'message': 'request is not allowed'}, 403)

    async def json_error(self):
        await self.json_response('404: Not Found', 404)

    async def insert_into_db(self, collection, data):
        db = self.settings['db']

        try:
            collection = db[collection]
        except:
            return None

        duplicate = await self._check_for_duplicate(collection, data)

        if duplicate is None:
            id_list = await collection.distinct('Id')

            new_id = max(id_list) + 1
            data['Id'] = new_id

            result = await collection.insert_one(data)
            return data['Id']

        else:
            return duplicate['Id']

    async def find_in_db(self, collection, query_filter=None):
        db = self.settings['db']

        try:
            collection = db[collection]
        except:
            return None

        if query_filter is None:
            cursor = collection.find().sort('Id')

        else:
            cursor = collection.find(query_filter).sort('Id')

        documents = await cursor.to_list(100)

        return documents

    async def update_into_db(self, collection, id, data):
        db = self.settings['db']

        try:
            collection = db[collection]
        except:
            return None

        # result = await collection.replace_one({'Id': id}, {'key': 'value'})
        result = await collection.update_one({'Id': id}, {'$set': data})

        return result.modified_count

    async def delete_from_db(self, collection, id):
        db = self.settings['db']

        try:
            collection = db[collection]
        except:
            return None

        result = await collection.delete_many({'Id': id})
        return result

    async def _check_for_duplicate(self, collection, data):
        document = await collection.find_one(data)
        return document

    async def _json_serialize(self, data):
        if isinstance(data, list):
            for i, chunk in enumerate(data):
                data[i] = await self._json_serialize(chunk)

        elif isinstance(data, dict):
            if '_id' in data:
                del data['_id']

            return data

        return json.dumps(data)


class MainHandler(BaseHandler):
    """Main Handler for service base url.

    Handler will redirect requests to swagger ui to provide information about
    the API.

    Otherwise block other CRUD functions with not allowed status.
    """

    async def get(self):
        self.redirect('/swagger/spec.html')
        return

    async def post(self, *args):
        await self.action_not_allowed()

    async def put(self, *args):
        await self.action_not_allowed()

    async def delete(self, *args):
        await self.action_not_allowed()


class ArtistsHandler(BaseHandler):
    """Artist Handler for serving Artists data.

    Endpoint for serving all artists.
    """

    async def get(self):
        """Return artists from our "database"
        ---
        tags: [Artists]
        summary: Get Artists
        description: Get all the artists.
            Accepts URL querystring notation to search on artist 'name'.
        responses:
            200:
                description: List of artists
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                ArtistSchema
        """

        name = self.get_argument('name', None)

        filter = None
        if name is not None:
            filter = {'Name': {'$regex': rf"(?i){name}"}}

        artists = await self.find_in_db('artists', query_filter=filter)

        await self.json_response(artists, 200)

    async def post(self):
        """Adds new artist into our "database"
        ---
        tags: [Artists]
        summary: Create a Artist
        description: Create a Artist
        requestBody:
            description: New Artist data
            required: True
            content:
                application/json:
                    schema:
                        ArtistCreateSchema
        responses:
            201:
                description: Success payload containing newly created Artist information
                content:
                    application/json:
                        schema:
                            ArtistCreateSuccessSchema
            400:
                description: Bad request; Check `errors` for any validation errors
                content:
                    application/json:
                        schema:
                            BadRequestSchema
        """

        try:
            new_artist = json.loads(self.request.body)

        except json.decoder.JSONDecodeError as e:
            await self.json_response({"success": False, "errors": str(e)}, 400)
            return

        validation_errors = ArtistSchema().validate(new_artist)

        if validation_errors:
            await self.json_response({"success": False, "errors": validation_errors}, 400)
            return

        else:
            result_id = await self.insert_into_db('artists', new_artist)
            new_artist['Id'] = result_id
            await self.json_response(new_artist, 201)


class ArtistHandler(BaseHandler):
    """Artists Handler for serving Artists data.

    Implements CRUD for artists data. Aggregrates actions to the database if needed.
    """

    async def get(self, slug):
        """Return artist from our "database" based on 'Id'
        ---
        tags: [Artists]
        summary: Get specific Artist
        description: Get specific artist based on 'Id'.
        responses:
            200:
                description: Dictionary of artist
                content:
                    application/json:
                        schema:
                            type: Dictionary
                            items:
                                ArtistSchema
        """
        filter = {'Id': int(slug)}
        artist = await self.find_in_db('artists', query_filter=filter)

        if len(artist) == 1:
            await self.json_response(artist[0], 200)

        else:
            await self.json_error()

    async def put(self, slug):
        """Update artist information in our "database"
        ---
        tags: [Artists]
        summary: Update a Artist
        description: Update a Artist
        requestBody:
            description: New Artist data
            required: True
            content:
                application/json:
                    schema:
                        ArtistCreateSchema
        responses:
            200:
                description: Success payload
            400:
                description: Bad request; Check `errors` for any validation errors
                content:
                    application/json:
                        schema:
                            BadRequestSchema
        """
        
        filter = {'Id': int(slug)}
        artist = await self.find_in_db('artists', query_filter=filter)

        if len(artist) == 0:
            await self.json_error()
            return

        try:
            new_artist_data = json.loads(self.request.body)
            artist = artist[0]

        except json.decoder.JSONDecodeError as e:
            await self.json_response({"success": False, "errors": str(e)}, 400)
            return

        validation_errors = ArtistSchema().validate(new_artist_data)

        if validation_errors:
            await self.json_response({"success": False, "errors": validation_errors}, 400)
            return

        else:
            result = await self.update_into_db('artists', artist['Id'], new_artist_data)
            if result != 0:
                await self.json_response('', 200)

    async def delete(self, slug):
        """Delete Artist from our "database"
        ---
        tags: [Artists]
        summary: Delete a Artist
        description: Delete a Artist
        responses:
            200:
                description: Success payload
            400:
                description: Bad request; Check `errors` for any validation errors
                content:
                    application/json:
                        schema:
                            BadRequestSchema
        """

        filter = {'Id': int(slug)}
        artist = await self.find_in_db('artists', query_filter=filter)

        if len(artist) == 0:
            await self.json_error()
            return

        artist = artist[0]

        result = await self.delete_from_db('artists', artist['Id'])

        await self.json_response('', 200)


class SongsHandler(BaseHandler):
    """Songs Handler for serving Songs data.

    Endpoint for serving all Songs.
    """

    async def get(self):
        """Return Songs from our "database"
        ---
        tags: [Songs]
        summary: Get Songs
        description: Get all the Songs.
            Accepts URL querystring notation to search on song 'name' and 'genre'
        responses:
            200:
                description: List of Songs
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                SongsSchema
        """

        name = self.get_argument('name', None)
        genre = self.get_argument('genre', None)

        filter = {}
        if name is not None:
            filter['Name'] = {'$regex': rf"(?i){name}"}

        if genre is not None:
            filter['Genre'] = {'$regex': rf"(?i){genre}"}

        if len(filter) == 0:
            filter = None

        songs = await self.find_in_db('songs', query_filter=filter)

        await self.json_response(songs, 200)

    async def post(self):
        """Adds new song into our "database"
        ---
        tags: [Songs]
        summary: Create a Song
        description: Create a Song
        requestBody:
            description: New Song data
            required: True
            content:
                application/json:
                    schema:
                        SongCreateSchema
        responses:
            201:
                description: Success payload containing newly created Song information
                content:
                    application/json:
                        schema:
                            SongCreateSuccessSchema
            400:
                description: Bad request; Check `errors` for any validation errors
                content:
                    application/json:
                        schema:
                            BadRequestSchema
        """

        try:
            new_song = json.loads(self.request.body)

        except json.decoder.JSONDecodeError as e:
            await self.json_response({"success": False, "errors": str(e)}, 400)
            return

        validation_errors = SongSchema().validate(new_song)

        if validation_errors:
            await self.json_response({"success": False, "errors": validation_errors}, 400)
            return

        else:
            result_id = await self.insert_into_db('songs', new_song)
            new_song['Id'] = result_id
            await self.json_response(new_song, 201)


class SongHandler(BaseHandler):
    """Songs Handler for serving Songs data.

    Implements CRUD for artists data. Aggregrates actions to the database if needed.
    """

    async def get(self, slug):
        """Return song from our "database" based on 'Id'
        ---
        tags: [Songs]
        summary: Get specific Song
        description: Get specific Song based on 'Id'.
        responses:
            200:
                description: Dictionary of Song
                content:
                    application/json:
                        schema:
                            type: Dictionary
                            items:
                                SongSchema
        """
        filter = {'Id': int(slug)}
        artist = await self.find_in_db('songs', query_filter=filter)

        if len(artist) == 1:
            await self.json_response(artist[0], 200)

        else:
            await self.json_error()

    async def put(self, slug):
        """Update Song information in our "database"
        ---
        tags: [Songs]
        summary: Update a Song
        description: Update a Song
        requestBody:
            description: New Song data
            required: True
            content:
                application/json:
                    schema:
                        SongCreateSchema
        responses:
            200:
                description: Success payload
            400:
                description: Bad request; Check `errors` for any validation errors
                content:
                    application/json:
                        schema:
                            BadRequestSchema
        """
        filter = {'Id': int(slug)}
        song = await self.find_in_db('songs', query_filter=filter)

        if len(song) == 0:
            await self.json_error()
            return

        try:
            new_song_data = json.loads(self.request.body)
            song = song[0]

        except json.decoder.JSONDecodeError as e:
            await self.json_response({"success": False, "errors": str(e)}, 400)
            return

        validation_errors = SongSchema().validate(new_song_data)

        if validation_errors:
            await self.json_response({"success": False, "errors": validation_errors}, 400)
            return

        else:
            result = await self.update_into_db('songs', song['Id'], new_song_data)
            if result != 0:
                await self.json_response('', 200)

    async def delete(self, slug):
        """Delete Song from our "database"
        ---
        tags: [Songs]
        summary: Delete a Song
        description: Delete a Song
        responses:
            200:
                description: Success payload
            400:
                description: Bad request; Check `errors` for any validation errors
                content:
                    application/json:
                        schema:
                            BadRequestSchema
        """
        filter = {'Id': int(slug)}
        song = await self.find_in_db('songs', query_filter=filter)

        if len(song) == 0:
            await self.json_error()
            return

        song = song[0]

        result = await self.delete_from_db('songs', song['Id'])

        await self.json_response('', 200)



