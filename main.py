from pathlib import Path

from aiohttp import web

from graph import generate_graph
from parser import parse_data
from views import view_all_paths, view_best_path

THIS_DIR = Path(__file__).parent
BASE_DIR = THIS_DIR.parent


def create_app():
    app = web.Application()

    @app.on_startup.append
    async def startup(app: web.Application):
        with open('RS_ViaOW.xml', 'r') as file:
            all_itinerary_viaow = parse_data(file)
        with open('RS_Via-3.xml', 'r') as file:
            all_itinerary_via3 = parse_data(file)
        all_itinerary = all_itinerary_via3 + all_itinerary_viaow
        app['graph'] = generate_graph(all_itinerary)

    app.add_routes([
        web.get('/all-paths/{source}/{destination}', view_all_paths),
        web.get('/best-path/{source}/{destination}', view_best_path),
    ])

    return app


web.run_app(create_app(), port=8000)
