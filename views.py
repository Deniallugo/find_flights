from aiohttp import web

from graph import FindType, SortType
from serializers import serialize


async def view_best_path(request):
    source = request.query.get('source')
    dest = request.query.get('dest')
    trip_type = request.query.get('trip_type', FindType.best)
    sort_type = request.query.get('sort', SortType.asc)
    if source and dest:
        graph = request.app['graph']

        trip = await request.app.loop.run_in_executor(
            None, graph.find_best_trip, source, dest, trip_type, sort_type)

        response = list(map(serialize, trip))

        return web.json_response(response)
    else:
        raise web.HTTPBadRequest(text='dest and source params not provided')


async def view_all_paths(request):
    source = request.query.get('source')
    dest = request.query.get('dest')
    if source and dest:
        graph = request.app['graph']

        all_paths = await request.app.loop.run_in_executor(
            None, graph.find_all_path, source, dest)

        response = list(map(serialize, all_paths))

        return web.json_response(response)
    else:
        raise web.HTTPBadRequest(text='dest and source params not provided')
