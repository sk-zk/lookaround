import math

TILE_SIZE = 256

def get_north_offset(unknown10, unknown11):
    """
    Calculates the longitude in the panorama which faces north.
    """
    MAX_UNKNOWN_10 = 16384
    UNKNOWN_11_MID = 8192

    if unknown10 >= 10000:
        unknown10 -= MAX_UNKNOWN_10

    unknown11 -= UNKNOWN_11_MID

    rad = math.atan2(unknown10, -unknown11) + 1.5 * math.pi
    rad %= (2 * math.pi)

    return rad


def protobuf_tile_offset_to_wgs84(x_offset, y_offset, tile_x, tile_y):
    """
    Calculates the absolute position of a pano from the tile offsets returned by the API.
    :param x_offset: The X coordinate of the raw tile offset returned by the API.
    :param y_offset: The Y coordinate of the raw tile offset returned by the API.
    :param tile_x: X coordinate of the tile this pano is on, at z=17.
    :param tile_y: Y coordinate of the tile this pano is on, at z=17.
    :return: The WGS84 lat/lon of the pano.
    """
    pano_x = tile_x + (x_offset / 64.0) / (TILE_SIZE - 1)
    pano_y = tile_y + (255 - (y_offset / 64.0)) / (TILE_SIZE - 1)
    lat, lon = tile_coord_to_wgs84(pano_x, pano_y, 17)
    return lat, lon


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


def mercator_to_wgs84(x, y):
    lat = (2 * math.atan(math.exp((y - 128) / -(256 / (2 * math.pi)))) - math.pi / 2) / (math.pi / 180)
    lon = (x - 128) / (256 / 360)
    return lat, lon


def tile_coord_to_wgs84(x, y, zoom):
    scale = 1 << zoom
    pixel_coord = (x * TILE_SIZE, y * TILE_SIZE)
    world_coord = (pixel_coord[0] / scale, pixel_coord[1] / scale)
    lat_lon = mercator_to_wgs84(world_coord[0], world_coord[1])
    return lat_lon
