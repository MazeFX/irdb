# -*- coding: utf-8 -*-
"""Handlers Collection.

Module containing all the used Request Handlers for the Tornado Server.
"""


from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    async def json_response(self, data, status_code=200):
        self.set_status(status_code)
        self.set_header("Content-Type", 'application/json')
        self.write(data)

    async def action_not_allowed(self):
        await self.json_response({'message': 'request is not allowed'}, 403)

    async def json_error(self):
        await self.json_response({'message': 'body is empty'}, 404)


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
