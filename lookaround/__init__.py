import requests
from requests import Session
from typing import List
import aiohttp
from aiohttp import ClientSession

from lookaround.proto import GroundMetadataTile_pb2
from .auth import Authenticator
from .panorama import LookaroundPanorama
from . import geo

COVERAGE_TILE_ENDPOINT = "https://gspe76-ssl.ls.apple.com/api/tile?"
PANO_FACE_ENDPOINT = "https://gspe72-ssl.ls.apple.com/mnn_us/"


def get_coverage_tile_by_latlon(lat: float, lon: float, session: Session = None) -> List[LookaroundPanorama]:
    x, y = geo.wgs84_to_tile_coord(lat, lon, 17)
    return get_coverage_tile(x, y, session=session)


async def get_coverage_tile_by_latlon_async(lat: float, lon: float, session: ClientSession = None) \
        -> List[LookaroundPanorama]:
    x, y = geo.wgs84_to_tile_coord(lat, lon, 17)
    return await get_coverage_tile_async(x, y, session)


def get_coverage_tile(tile_x: int, tile_y: int, session: Session = None) -> List[LookaroundPanorama]:
    tile = _get_coverage_tile_raw(tile_x, tile_y, session=session)
    return _parse_coverage_tile(tile, tile_x, tile_y)


async def get_coverage_tile_async(tile_x: int, tile_y: int, session: ClientSession = None) -> List[LookaroundPanorama]:
    tile = await _get_coverage_tile_raw_async(tile_x, tile_y, session)
    return _parse_coverage_tile(tile, tile_x, tile_y)


def _parse_coverage_tile(tile: GroundMetadataTile_pb2.GroundMetadataTile, tile_x: int, tile_y: int) \
        -> List[LookaroundPanorama]:
    panos = []
    for pano in tile.pano:
        lat, lon = geo.protobuf_tile_offset_to_wgs84(
            pano.tile_position.x,
            pano.tile_position.y,
            tile_x,
            tile_y)
        heading = geo.convert_heading(lat, lon, pano.tile_position.yaw)
        camera_metadata = [tile.camera_metadata[x] for x in pano.camera_metadata_idx]
        pano_obj = LookaroundPanorama(
            panoid=pano.panoid,
            build_id=tile.build_table[pano.build_table_idx].build_id,
            lat=lat,
            lon=lon,
            heading=heading,
            camera_metadata=camera_metadata,
            elevation=geo.convert_altitude(pano.tile_position.altitude, lat, lon, tile_x, tile_y),
            coverage_type=tile.build_table[pano.build_table_idx].coverage_type,
            timestamp=pano.timestamp,
            has_blurs=tile.build_table[pano.build_table_idx].index != 0,
        )
        # pano_obj.dbg = (pano.tile_position.yaw, pano.tile_position.pitch, pano.tile_position.roll)
        panos.append(pano_obj)
    return panos


def _get_coverage_tile_raw(tile_x: int, tile_y: int, session: Session = None) \
        -> GroundMetadataTile_pb2.GroundMetadataTile:
    headers = _create_coverage_tile_request_headers(tile_x, tile_y)
    requester = session if session else requests
    response = requester.get(COVERAGE_TILE_ENDPOINT, headers=headers)
    return _parse_coverage_tile_response(response.content)


async def _get_coverage_tile_raw_async(tile_x: int, tile_y: int, session: ClientSession = None) \
        -> GroundMetadataTile_pb2.GroundMetadataTile:
    if session is None:
        async with aiohttp.ClientSession() as session:
            return await _get_coverage_tile_raw_async(tile_x, tile_y, session)

    headers = _create_coverage_tile_request_headers(tile_x, tile_y)
    async with session.get(COVERAGE_TILE_ENDPOINT, headers=headers) as response:
        content = await response.read()
        return _parse_coverage_tile_response(content)


def _create_coverage_tile_request_headers(tile_x: int, tile_y: int) -> dict:
    return {
        "maps-tile-style": "style=57&size=2&scale=0&v=0&preflight=2",
        "maps-tile-x": str(tile_x),
        "maps-tile-y": str(tile_y),
        "maps-tile-z": "17",
        "maps-auth-token": "w31CPGRO/n7BsFPh8X7kZnFG0LDj9pAuR8nTtH3xhH8=",
    }


def _parse_coverage_tile_response(content: bytes) -> GroundMetadataTile_pb2.GroundMetadataTile:
    tile = GroundMetadataTile_pb2.GroundMetadataTile()
    tile.ParseFromString(content)
    return tile


def get_pano_face(panoid: int, build_id: int, face: int, zoom: int,
                  auth: Authenticator, session: Session = None) -> bytes:
    url = build_pano_face_url(panoid, build_id, face, zoom, auth)
    requester = session if session else requests
    response = requester.get(url)
        
    if response.ok:
        return response.content
    else:
        response.raise_for_status()


# Tried to get this to work, but I'm out of ideas. Just 403s every time.
# The URL is correct, the headers aren't the issue, and I'm out of ideas at this point.
"""
async def get_pano_face_async(panoid: int, region_id: int, face: int, zoom: int,
                               auth: Authenticator, session: ClientSession = None) -> bytes:
    if session is None:
        async with aiohttp.ClientSession() as session:
            return await get_pano_face_async(panoid, region_id, face, zoom, auth, session)

    url = _build_pano_face_url(panoid, region_id, face, zoom, auth)
    print(url)
    async with session.get(url) as response:
        content = await response.read()
        return content
"""


def build_pano_face_url(panoid: int, build_id: int, face: int, zoom: int, auth: Authenticator) -> str:
    if face > 5:
        raise ValueError("Faces range from 0 to 5 inclusive.")
    zoom = min(7, zoom)

    panoid, build_id = _panoid_to_string(panoid, build_id)

    url = PANO_FACE_ENDPOINT + f"{panoid}/{build_id}/t/{face}/{zoom}"
    url = auth.authenticate_url(url)
    return url


def _panoid_to_string(panoid, build_id):
    panoid = str(panoid)
    build_id = str(build_id)
    if len(panoid) > 20:
        raise ValueError("panoid must not be longer than 20 digits.")
    if len(build_id) > 10:
        raise ValueError("build_id must not be longer than 10 digits.")

    panoid_padded = panoid.zfill(20)
    panoid_split = [panoid_padded[i:i + 4] for i in range(0, len(panoid_padded), 4)]
    panoid_url = "/".join(panoid_split)
    build_id_padded = build_id.zfill(10)

    return panoid_url, build_id_padded


def get_mt7_file(panoid, build_id, auth, session=None):
    panoid, build_id = _panoid_to_string(panoid, build_id)

    url = PANO_FACE_ENDPOINT + f"{panoid}/{build_id}/mt/7"
    url = auth.authenticate_url(url)
    if session:
        response = session.get(url)
    else:
        response = requests.get(url)
        
    if response.ok:
        return response.content
    else:
        raise Exception(str(response))


def get_m_file(panoid, build_id, zoom, auth, session=None):
    panoid, build_id = _panoid_to_string(panoid, build_id)

    url = PANO_FACE_ENDPOINT + f"{panoid}/{build_id}/m/{zoom}"
    url = auth.authenticate_url(url)
    if session:
        response = session.get(url)
    else:
        response = requests.get(url)

    if response.ok:
        return response.content
    else:
        raise Exception(str(response))
