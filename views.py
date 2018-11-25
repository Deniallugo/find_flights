from aiohttp import web

from graph import FindType
from serializers import serialize


async def handle(request):
    source = request.query.get('source')
    dest = request.query.get('dest')
    trip_type = request.query.get('trip_type', FindType.best)
    if source and dest:
        graph = request.app['graph']

        trip = await request.app.loop.run_in_executor(
            None, graph.find_best_trip, source, dest, trip_type)
        response = list(map(serialize, trip))

        return web.json_response(response)
    else:
        raise web.HTTPBadRequest(text='dest and source params not provided')
