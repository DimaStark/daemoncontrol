#!/usr/bin/python3
""" Main entry """

from os import path

import asyncio
import aiohttp
from aiohttp import web

__dir__ = path.dirname(path.realpath(__file__))


async def websocket_handler(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws


def main():
    loop = asyncio.get_event_loop()
    app = web.Application(loop=loop)
    app.router.get('/ws', websocket_handler)
    web.run_app(app, host='127.0.0.1', port=8080)


if __name__ == '__main__':
    main()
