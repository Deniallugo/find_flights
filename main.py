from pathlib import Path

from aiohttp import web

from graph import generate_graph
from parser import parse_data
from views import handle

THIS_DIR = Path(__file__).parent
BASE_DIR = THIS_DIR.parent


def create_app():
    app = web.Application()

    @app.on_startup.append
    async def startup(app: web.Application):
        with open('RS_Via-3.xml', 'r') as file:
            all_itinerary = parse_data(file)
            app['graph'] = generate_graph(all_itinerary)

    app.add_routes([web.get('/', handle)])

    return app


web.run_app(create_app(), port=8000)
