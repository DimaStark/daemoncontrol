#!/usr/bin/python3
""" Main entry """

from os import path

import asyncio
from aiohttp import web

from web.views import index

__dir__ = path.dirname(path.realpath(__file__))


def add_routes(app: web.Application) -> web.Application:
    app.router.add_static('/static/', path.join(__dir__, '..', 'static'))
    app.router.add_get('/', index)

    return app


def main():
    loop = asyncio.get_event_loop()
    app = add_routes(web.Application(loop=loop))
    web.run_app(app, host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
