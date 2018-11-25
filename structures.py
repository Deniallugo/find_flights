from collections import namedtuple
from enum import Enum

Flight = namedtuple('Flight', (
    'Carrier', 'FlightNumber',
    'Source', 'Destination',
    'DepartureTimeStamp', 'ArrivalTimeStamp',
    'Class', 'NumberOfStops', 'FareBasis',
    'WarningText', 'TicketType',
))


class Itinerary(namedtuple('Itinerary', (
        'Source', 'Destination',
        'DepartureTimeStamp', 'ArrivalTimeStamp',
        'TotalPrice', 'Flights', 'ReturnedItinerary',
        # 'WaitTime' Should we count it ?
))):

    def __eq__(self, other):
        """
        It's possibly true, but I don't know. Of course it's not for production.
        But there are a lot of the same Itinerary here
        """
        return (self.Source == other.Source and
                self.Destination == other.Destination and
                self.DepartureTimeStamp == other.DepartureTimeStamp and
                self.ArrivalTimeStamp == other.ArrivalTimeStamp and
                self.TotalPrice == other.TotalPrice)


class FindType(Enum):
    price = 1
    time = 2
    best = 3


class DirectionType(Enum):
    desc = 1
    asc = 2
