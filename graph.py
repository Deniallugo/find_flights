from settings import weight_seconds, weight_price, inf
from structures import FindType


def cost_of_itinerary(itinerary, trip_type: FindType):
    time_cost = (itinerary.DepartureTimeStamp -
                 itinerary.ArrivalTimeStamp).seconds * weight_seconds
    price_cost = itinerary.TotalPrice * weight_price
    if trip_type == FindType.time:
        return time_cost
    elif trip_type == FindType.price:
        return price_cost
    else:
        return price_cost + time_cost


def possible_itinerary(from_itinerary, to_itinerary):
    """
    We can have some more rules,
    for example difference between arrival and departure can be 1 hour or more.
    :param from_itinerary:
    :param to_itinerary:
    :return:
    """
    if from_itinerary:
        return from_itinerary.ArrivalTimeStamp < to_itinerary.DepartureTimeStamp
    else:
        return True


def find_best_itinerary(itineraries, from_itinerary, trip_type):
    best_cost = float('inf')
    best_itinerary = None
    for itinerary in itineraries:
        if possible_itinerary(from_itinerary, itinerary):
            cost = cost_of_itinerary(itinerary, trip_type)
            if cost < best_cost:
                best_cost = cost
                best_itinerary = itinerary

    return best_itinerary, best_cost


class Graph(object):

    def __init__(self):
        self._graph_dict = {}

    def vertices(self):
        return list(self._graph_dict.keys())

    def add_vertex(self, vertex):

        if vertex not in self._graph_dict:
            self._graph_dict[vertex] = []

    def add_itinerary(self, itinerary):
        source_vertex = itinerary.Source
        destination_vertex = itinerary.Destination
        if source_vertex in self._graph_dict:
            if destination_vertex in self._graph_dict[source_vertex]:
                self._graph_dict[source_vertex][destination_vertex].append(
                    itinerary)
            else:
                self._graph_dict[source_vertex][destination_vertex] = [
                    itinerary]
        else:
            self._graph_dict[source_vertex] = {destination_vertex: [itinerary]}

    def find_best_trip(self, source, dest, trip_type, onward_trip=None):
        distances = {vertex: inf for vertex in self._graph_dict.keys()}
        vertices = list(self._graph_dict.keys())

        previous_vertices = {
            vertex: None for vertex in vertices
        }

        itineraries_path = {}

        distances[source] = 0
        from_itinerary = None
        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break

            for neighbour, itineraries in \
                    self._graph_dict[current_vertex].items():

                from_itinerary, cost = find_best_itinerary(itineraries,
                                                           from_itinerary,
                                                           trip_type)
                alternative_route = distances[current_vertex] + cost

                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex
                    itineraries_path[neighbour] = from_itinerary

        current_vertex = dest
        path = []

        while previous_vertices[current_vertex] is not None:
            path.append(itineraries_path[current_vertex])
            current_vertex = previous_vertices[current_vertex]

        path.reverse()

        return path

    def find_all_path(self, source, dest):
        pass


def generate_graph(all_itinerary):
    graph = Graph()
    for itinerary in all_itinerary:
        graph.add_itinerary(itinerary)
    return graph
