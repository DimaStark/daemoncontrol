from aiohttp import web
from daemonctl.service import Service

SERVICE = Service()
HTML = r'''
    <!doctype html>
    <html lang="ru">
    <head>
        <meta charset="utf-8">
        <title>Daemon control</title>
        <style>
            .on {{ color: green }}
            .off {{ color: red }}
            table {{
                border: 1px solid black;
                border-collapse: collapse;
            }}
            td {{
                padding: 10px;
                border: 1px solid black;
            }}
        </style>
    </head>
    <body><table>
        {}
    </table></body>
    </html>
'''


async def websocket_handler(request):
    # TODO: Написать работу на вебсокетах
    response_html = HTML.format(SERVICE.to_html())
    return web.Response(
        text=response_html,
        content_type='text/html',
    )
