from collections import namedtuple
from enum import Enum

Flight = namedtuple('Flight', (
    'Carrier', 'FlightNumber',
    'Source', 'Destination',
    'DepartureTimeStamp', 'ArrivalTimeStamp',
    'Class', 'NumberOfStops', 'FareBasis',
    'WarningText', 'TicketType',
))

Itinerary = namedtuple('Itinerary', (
    'Source', 'Destination',
    'DepartureTimeStamp', 'ArrivalTimeStamp',
    'TotalPrice', 'Flights', 'ReturnedItinerary',
    # 'WaitTime' Should we count it ?
))


class FindType(Enum):
    price = 1
    time = 2
    best = 3


class SortType(Enum):
    desc = 1
    asc = 2
