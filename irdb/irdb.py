# -*- coding: utf-8 -*-
"""Main Application module.

Module that start the Tornado Server when run.
"""


import swagger_ui
import tornado.ioloop
import tornado.web
import motor

try:
    from .app.handlers import MainHandler, ArtistHandler, ArtistsHandler, SongHandler, SongsHandler
    from .init_swagger import generate_swagger_file

except:
    from app.handlers import MainHandler, ArtistHandler, ArtistsHandler, SongHandler, SongsHandler
    from init_swagger import generate_swagger_file

SWAGGER_API_OUTPUT_FILE = "./swagger.json"


def make_app():
    """Make a Tornado App Instance.

    Creates an Tornado app with all the default handlers needed for the API.

    Returns:
        obj: Tornado web app

    """

    handlers = [
        (r"/", MainHandler),
        (r"/artists", ArtistsHandler),
        (r"/artists/([0-9]+)", ArtistHandler),
        (r"/songs", SongsHandler),
        (r"/songs/([0-9]+)", SongHandler),
    ]

    # Initialize Tornado application
    client = motor.motor_tornado.MotorClient(f'mongodb://root:rootpwd@mongodb:27017')
    app = tornado.web.Application(handlers, db=client.test)

    # Generate a fresh Swagger file
    generate_swagger_file(handlers=handlers, file_location=SWAGGER_API_OUTPUT_FILE)

    # Start the Swagger UI. Automatically generated swagger.json can also
    # be served using a separate Swagger-service.
    swagger_ui.tornado_api_doc(
        app,
        config_path=SWAGGER_API_OUTPUT_FILE,
        url_prefix="/swagger/spec.html",
        title="Internet Rock Database API",
    )

    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()