from aiohttp import web

from graph import FindType, DirectionType
from serializers import serialize


async def view_best_path(request):
    source = request.match_info.get('source')
    dest = request.match_info.get('destination')
    trip_type = request.query.get('trip_type', FindType.best)
    direction_type = request.query.get('sort', DirectionType.asc)

    graph = request.app['graph']
    try:
        trip = await request.app.loop.run_in_executor(
            None, graph.find_best_trip, source, dest, trip_type,
            direction_type)
    except KeyError as e:
        response = {'error': f'{e.args[0]} not find'}
    else:
        response = list(map(serialize, trip))

    return web.json_response(response)


async def view_all_paths(request):
    source = request.match_info.get('source')
    dest = request.match_info.get('destination')

    graph = request.app['graph']
    try:
        all_paths = await request.app.loop.run_in_executor(
            None, graph.find_all_path, source, dest)
    except KeyError as e:
        response = {'error': f'{e.args[0]} not find'}
    else:
        response = list(map(serialize, all_paths))

    return web.json_response(response)
