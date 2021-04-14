# -*- coding: utf-8 -*-
"""Main Application module.

Module that start the Tornado Server when run.
"""

import tornado.ioloop
import tornado.web

from .app.handlers import MainHandler


def make_app():
    """Make a Tornado App Instance.

    Creates an Tornado app with all the default handlers needed for the API.

    Returns:
        obj: Tornado web app

    """

    handlers = [
        (r"/", MainHandler),
    ]

    # Initialize Tornado application
    app = tornado.web.Application(handlers)

    return app


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()