from aiohttp import web


async def handle(request):
    return web.Response(text="Hello from aiohttp!")


def main():
    app = web.Application()
    app.router.add_get('/', handle)
    web.run_app(app,
                host='0.0.0.0',
                port=8000)


if __name__ == '__main__':
    main()
