#!/usr/bin/python3
""" Main entry of the server """
import asyncio
from aiohttp import web

from daemonctl.views import websocket_handler


def main():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    app.router.add_get('/', websocket_handler)
    web.run_app(app, host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
