import requests
from requests import Session
from typing import List
import aiohttp
from aiohttp import ClientSession

from lookaround.proto import MapTile_pb2
from .auth import Authenticator
import lookaround.geo
from .panorama import LookaroundPanorama

COVERAGE_TILE_ENDPOINT = "https://gspe76-ssl.ls.apple.com/api/tile?"
PANO_FACE_ENDPOINT = "https://gspe72-ssl.ls.apple.com/mnn_us/"


def get_coverage_tile_by_latlon(lat: float, lon: float, session: Session = None) -> List[LookaroundPanorama]:
    x, y = geo.wgs84_to_tile_coord(lat, lon, 17)
    return get_coverage_tile(x, y, session=session)


async def get_coverage_tile_by_latlon_async(lat: float, lon: float, session: ClientSession = None) -> List[LookaroundPanorama]:
    x, y = geo.wgs84_to_tile_coord(lat, lon, 17)
    return await get_coverage_tile_async(x, y, session)


def get_coverage_tile(tile_x: int, tile_y: int, session: Session = None) -> List[LookaroundPanorama]:
    tile = _get_coverage_tile_raw(tile_x, tile_y, session=session)
    return _parse_coverage_tile(tile, tile_x, tile_y)


async def get_coverage_tile_async(tile_x: int, tile_y: int, session: ClientSession = None) -> List[LookaroundPanorama]:
    tile = await _get_coverage_tile_raw_async(tile_x, tile_y, session)
    return _parse_coverage_tile(tile, tile_x, tile_y)


def _parse_coverage_tile(tile: MapTile_pb2.MapTile, tile_x: int, tile_y: int) -> List[LookaroundPanorama]:
    panos = []
    for pano in tile.pano:
        lat, lon = geo.protobuf_tile_offset_to_wgs84(
            pano.location.longitude_offset,
            pano.location.latitude_offset,
            tile_x,
            tile_y)
        heading = geo.convert_heading(lat, lon, pano.location.heading)
        projection = [tile.projection[x] for x in pano.projection_idx]
        pano_obj = LookaroundPanorama(
            panoid=pano.panoid,
            batch_id=tile.unknown13[pano.batch_id_idx].batch_id,
            lat=lat,
            lon=lon,
            heading=heading,
            projection=projection,
            raw_elevation=pano.location.elevation,
            coverage_type=tile.unknown13[pano.batch_id_idx].coverage_type,
            timestamp=pano.timestamp,
            has_blurs=tile.unknown13[pano.batch_id_idx].unknown14 != 0,
        )
        pano_obj.dbg = (pano.location.heading, pano.location.unknown10, pano.location.unknown11)
        panos.append(pano_obj)
    return panos


def _get_coverage_tile_raw(tile_x: int, tile_y: int, session: Session = None) -> MapTile_pb2.MapTile:
    headers = _create_coverage_tile_request_headers(tile_x, tile_y)
    requester = session if session else requests
    response = requester.get(COVERAGE_TILE_ENDPOINT, headers=headers)
    return _parse_coverage_tile_response(response.content)


async def _get_coverage_tile_raw_async(tile_x: int, tile_y: int, session: ClientSession = None) -> MapTile_pb2.MapTile:
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


def _parse_coverage_tile_response(content: bytes) -> MapTile_pb2.MapTile:
    tile = MapTile_pb2.MapTile()
    tile.ParseFromString(content)
    return tile


def get_pano_face(panoid: int, batch_id: int, face: int, zoom: int,
                  auth: Authenticator, session: Session = None) -> bytes:
    url = build_pano_face_url(panoid, batch_id, face, zoom, auth)
    requester = session if session else requests
    response = requester.get(url)
        
    if response.ok:
        return response.content
    else:
        raise Exception(str(response))


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


def build_pano_face_url(panoid: int, batch_id: int, face: int, zoom: int, auth: Authenticator) -> str:
    if face > 5:
        raise ValueError("Faces range from 0 to 5 inclusive.")
    zoom = min(7, zoom)

    panoid, batch_id = _panoid_to_string(panoid, batch_id)

    url = PANO_FACE_ENDPOINT + f"{panoid}/{batch_id}/t/{face}/{zoom}"
    url = auth.authenticate_url(url)
    return url


def _panoid_to_string(panoid, batch_id):
    panoid = str(panoid)
    batch_id = str(batch_id)
    if len(panoid) > 20:
        raise ValueError("panoid must not be longer than 20 digits.")
    if len(batch_id) > 10:
        raise ValueError("batch_id must not be longer than 10 digits.")

    panoid_padded = panoid.zfill(20)
    panoid_split = [panoid_padded[i:i + 4] for i in range(0, len(panoid_padded), 4)]
    panoid_url = "/".join(panoid_split)
    batch_id_padded = batch_id.zfill(10)

    return panoid_url, batch_id_padded


def get_mt7_file(panoid, batch_id, auth, session=None):
    panoid, batch_id = _panoid_to_string(panoid, batch_id)

    url = PANO_FACE_ENDPOINT + f"{panoid}/{batch_id}/mt/7"
    url = auth.authenticate_url(url)
    if session:
        response = session.get(url)
    else:
        response = requests.get(url)
        
    if response.ok:
        return response.content
    else:
        raise Exception(str(response))


def get_m_file(panoid, batch_id, zoom, auth, session=None):
    panoid, batch_id = _panoid_to_string(panoid, batch_id)

    url = PANO_FACE_ENDPOINT + f"{panoid}/{batch_id}/m/{zoom}"
    url = auth.authenticate_url(url)
    if session:
        response = session.get(url)
    else:
        response = requests.get(url)

    if response.ok:
        return response.content
    else:
        raise Exception(str(response))
