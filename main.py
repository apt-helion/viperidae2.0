#!env/bin/python
from aiohttp import web
from routes import setup_routes

async def factory():
    app = web.Application()
    setup_routes(app)
    return app

if __name__ == "__main__":
    app = web.Application()
    setup_routes(app)
    web.run_app(app)
