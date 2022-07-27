import math
import requests

from lookaround.proto import MapTile_pb2
from .auth import Authenticator


def get_coverage_tile(tile_x, tile_y):
    headers = {
        "maps-tile-style": "style=57&size=2&scale=0&v=0&preflight=2",
        "maps-tile-x": str(tile_x),
        "maps-tile-y": str(tile_y),
        "maps-tile-z": "17",
        "maps-auth-token": "w31CPGRO/n7BsFPh8X7kZnFG0LDj9pAuR8nTtH3xhH8=",
    }
    response = requests.get("https://gspe76-ssl.ls.apple.com/api/tile?", headers=headers)
    tile = MapTile_pb2.MapTile()
    tile.ParseFromString(response.content)
    return tile


def get_coverage_tile_by_latlon(lat, lon):
    x, y = wgs84_to_tile_coord(lat, lon, 17)
    return get_coverage_tile(x, y)


def fetch_pano_segment(panoid, that_other_id, segment, zoom, auth):
    endpoint = "https://gspe72-ssl.ls.apple.com/mnn_us/"
    panoid = str(panoid)
    if (len(panoid) > 20):
        raise ValueError("panoid must not be longer than 20 characters.")
    if (segment > 5):
        raise ValueError("Segments range from 0 to 5 inclusive.")
    
    zoom = min(7, zoom)
    panoid_padded = str(panoid).zfill(20)
    panoid_split =  [panoid_padded[i:i+4] for i in range(0, len(panoid_padded), 4)]
    panoid_url = "/".join(panoid_split)
    url = endpoint + f"{panoid_url}/{that_other_id}/t/{segment}/{zoom}"
    url = auth.authenticate_url(url)
    response = requests.get(url)
    if response.ok:
        return response.content
    else:
        raise Exception(str(response))



TILE_SIZE = 256

def wgs84_to_tile_coord(lat, lon, zoom):
    scale = 1 << zoom
    world_coord = wgs84_to_mercator(lat, lon)
    pixel_coord = (math.floor(world_coord[0] * scale), math.floor(world_coord[1] * scale))
    tile_coord = (math.floor((world_coord[0] * scale) / TILE_SIZE), math.floor((world_coord[1] * scale) / TILE_SIZE))
    return tile_coord


def wgs84_to_mercator(lat, lon):
    siny = math.sin((lat * math.pi) / 180.0)
    siny = min(max(siny, -0.9999), 0.9999)
    return (
        TILE_SIZE * (0.5 + lon / 360.0),
        TILE_SIZE * (0.5 - math.log((1 + siny) / (1 - siny)) / (4 * math.pi))
    )
