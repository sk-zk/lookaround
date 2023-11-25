# Code for making requests against dispatcher.arpc.
# Based on some function names I've seen, Apple appears to calls these things "tickets",
# but I'm not entirely certain about that

import io
from dataclasses import dataclass

import requests
from requests import Session

from .binary import BinaryWriter, BinaryReader


@dataclass
class TicketRequestHeader:
    """
    Represents the header of a ticket request.
    """
    version_maybe: int = 1
    language: str = "en-US"
    app_identifier: str = "com.apple.geod"
    os_version: str = "11.7.5.20G1225"
    unknown: int = 60  # possibly a function ID


@dataclass
class TicketResponseHeader:
    """
    Represents the header of a ticket response.
    """
    version_maybe: int
    unknown: int


@dataclass
class TicketResponse:
    """
    Represents a ticket response.
    """
    header: TicketResponseHeader
    payload: bytes


def make_ticket_request(payload: bytes, session: Session = None) -> bytes:
    """
    Makes a request against dispatcher.arpc with the given payload.

    :param payload: The request payload.
    :return: The response payload.
    """
    header = TicketRequestHeader()
    request_body = serialize_ticket_request(header, payload)
    requester = session if session else requests
    http_response = requester.post("https://gsp-ssl.ls.apple.com/dispatcher.arpc", data=request_body)
    response_ticket = deserialize_ticket_response(http_response.content)
    return response_ticket.payload


def serialize_ticket_request(header: TicketRequestHeader, payload: bytes) -> bytes:
    """
    Creates the POST body of a ticket request.

    :param header: The ticket header.
    :param payload: The payload.
    :return: The serialized body.
    """
    w = BinaryWriter(io.BytesIO())
    w.write_uint2_be(header.version_maybe)
    _write_pascal_string_be(w, header.language)
    _write_pascal_string_be(w, header.app_identifier)
    _write_pascal_string_be(w, header.os_version)
    w.write_uint4_be(header.unknown)
    w.write_uint4_be(len(payload))
    w.write(payload)
    return w.content


def deserialize_ticket_response(response: bytes) -> TicketResponse:
    """
    Deserializes a ticket response.

    :param response: The response body.
    :return: The deserialized response.
    """
    r = BinaryReader(io.BytesIO(response))
    header = TicketResponseHeader(
        version_maybe=r.read_uint2_be(),
        unknown=r.read_uint4_be()
    )
    length = r.read_uint4_be()
    payload = r.read(length)
    return TicketResponse(header=header, payload=payload)


def _write_pascal_string_be(writer: BinaryWriter, value: str, encoding: str = "utf-8") -> None:
    value_bytes = value.encode(encoding)
    writer.write_uint2_be(len(value_bytes))
    writer.write(value_bytes)
