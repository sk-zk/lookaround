from typing import List

from requests import Session

from .ticket import make_ticket_request
from lookaround.proto import PlaceRequest_pb2, PlaceResponse_pb2, Shared_pb2


def _reverse_geocode_build_pb_request(lat: float, lon: float, display_languages: List[str]):
    pr = PlaceRequest_pb2.PlaceRequest()

    pr.display_language.extend(display_languages)
    # this must be set to get maps_result rather than legacy_place_result
    pr.client_metadata.supported_maps_result_type.append(Shared_pb2.MapsResultType.MAPS_RESULT_TYPE_PLACE)

    pr.request_type = PlaceRequest_pb2.RequestType.REQUEST_TYPE_REVERSE_GEOCODING
    pr.place_request_parameters.reverse_geocoding_parameters.preserve_original_location = True
    pr.place_request_parameters.reverse_geocoding_parameters.extended_location.lat_lng.lat = lat
    pr.place_request_parameters.reverse_geocoding_parameters.extended_location.lat_lng.lng = lon
    pr.place_request_parameters.reverse_geocoding_parameters.extended_location.vertical_accuracy = -1
    pr.place_request_parameters.reverse_geocoding_parameters.extended_location.heading = -1

    # specify what we want the server to return; 31 is the address
    rc = PlaceRequest_pb2.ComponentInfo()
    rc.type = 31
    rc.count = 1
    pr.request_component.append(rc)
    return pr


def reverse_geocode(lat: float, lon: float, display_language: List[str], session: Session = None):
    pb_request = _reverse_geocode_build_pb_request(lat, lon, display_language)

    response = make_ticket_request(pb_request.SerializeToString(), session)
    place_response = PlaceResponse_pb2.PlaceResponse()
    place_response.ParseFromString(response)

    address = place_response.maps_result.place.component[0].value[0].address_object.address_object.address
    return list(address.address.address_line)
