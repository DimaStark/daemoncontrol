from os import path

from aiohttp import web
from aiofiles import open as open_async


async def read_index_html_async() -> str:
    dir_path = path.dirname(path.realpath(__file__))
    index_html_path = path.join(dir_path, '..', 'static', 'index.html')
    async with open_async(index_html_path, mode='r') as html:
        return await html.read()


async def index(unused) -> web.Response:
    response_html = await read_index_html_async()

    return web.Response(
        text=response_html,
        content_type='text/html',
    )
