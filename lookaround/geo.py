import math


TILE_SIZE = 256


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


'''
Approximate heading of the panorama, assuming the POV is facing 
to the left of the Apple Car in cthe direction of driving.
'''
def heading_from_unkown10_unknown11(unknown10, unknown11):
    # Whatever is the logic behind this? 
    # Who at Apple thought of these values? 

    # TODO: Finetune these values
    # unknown10
    # These are the extreme values of unkown10 I have observed in a random selection of about 1000 tiles.
    # The values are in two clusters. 
    # In the range [1,2159] you're looking more west than east.
    # In the range [14318,16383] you're looking more east than west.
    westmin = 1
    westmax = 2159
    eastmin = 16383 # looking (north/south) and very slightly east
    eastmax = 14318 # looking slightly (north/south) directly east

    # unknown11
    # This is slightly more speculative
    northmin = 8204 # this is likely lower
    northmax = 6054
    southmin = 8204 # this is likely lower
    southmax = 10173


    ew=0
    if unknown10 < westmax:
        # Looking west
        ew = -(float(unknown10 - westmin) / float(westmax - westmin))
    elif unknown10 > eastmax:
        # Looking east
        ew = (float(unknown10 - eastmin) / float(eastmax - eastmin))

    ns=0
    if unknown11 <= northmin:
        # Looking north
        ns = (float(unknown11 - northmin) / float(northmax - northmin))
    else:
        ns = -(float(unknown11 - southmin) / float(southmax - southmin))


    print(ns,ew)
    r =  math.degrees(math.atan2(ew,ns))
    if r < 0:
        r += 360
    return r
