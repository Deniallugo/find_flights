import datetime
from typing import List
from xml.etree import ElementTree

from settings import datetime_format
from structures import Itinerary, Flight


def convert_string_to_dt(date_string):
    return datetime.datetime.strptime(date_string, datetime_format)


def generate_itinerary(flights: List[Flight], price, returned_itinerary_id):
    first_flight = flights[0]
    last_flight = flights[-1]
    itinerary = Itinerary(
        Source=first_flight.Source,
        Destination=last_flight.Destination,
        ArrivalTimeStamp=last_flight.ArrivalTimeStamp,
        DepartureTimeStamp=first_flight.DepartureTimeStamp,
        Flights=flights,
        ReturnedItinerary=returned_itinerary_id,
        TotalPrice=price,
    )
    return itinerary


def parse_itinerary(itinerary_xml, price, returned_itinerary_id):
    flights = itinerary_xml.find('Flights')
    itinerary_flights = []
    for flight_data in flights:
        itinerary_flights.append(Flight(
            Carrier=flight_data.find('Carrier').text,
            FlightNumber=flight_data.find('FlightNumber').text,
            Source=flight_data.find('Source').text,
            Destination=flight_data.find('Destination').text,
            DepartureTimeStamp=convert_string_to_dt(
                flight_data.find('DepartureTimeStamp').text),
            ArrivalTimeStamp=convert_string_to_dt(
                flight_data.find('ArrivalTimeStamp').text),
            Class=flight_data.find('Class').text,
            NumberOfStops=flight_data.find('NumberOfStops').text,
            FareBasis=flight_data.find('FareBasis').text,
            WarningText=flight_data.find('WarningText').text,
            TicketType=flight_data.find('TicketType').text,
        ))
    return generate_itinerary(itinerary_flights, price, returned_itinerary_id)


def parse_data(xml_data):
    all_itinerary = []
    data = ElementTree.parse(xml_data)
    for itinerary_data in data.find('PricedItineraries'):
        last_itinerary_id = len(all_itinerary) - 1
        onward_itinerary_data = itinerary_data.find('OnwardPricedItinerary')
        return_itinerary_data = itinerary_data.find('ReturnPricedItinerary')
        price = itinerary_data.find('Pricing')
        total_price = None
        for service_charge in price.findall('ServiceCharges'):
            if service_charge.attrib['ChargeType'] == 'TotalAmount':
                total_price = float(service_charge.text)
                break
        onward_itinerary = parse_itinerary(onward_itinerary_data, total_price,
                                           last_itinerary_id + 2)
        all_itinerary.append(onward_itinerary)
        return_itinerary = parse_itinerary(return_itinerary_data, total_price,
                                           last_itinerary_id + 1)
        all_itinerary.append(return_itinerary)
        # Now we think, that we have the same currency for all itinerary

    return all_itinerary
