import math
from typing import Tuple
import numpy as np
import pyproj
from pyproj import Transformer
from scipy.spatial.transform import Rotation


pyproj.network.set_network_enabled(active=True)
TILE_SIZE = 256
tf_web_mercator_to_ecef = Transformer.from_crs(3857, 4978)
tf_wgs84_to_wgs84_egm2008 = Transformer.from_crs(4979, 9518)
tf_wgs84_to_ecef = Transformer.from_crs(4326, 4978)


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


def wgs84_to_tile_coord(lat: float, lon: float, zoom: int) -> Tuple[int, int]:
    """
    Converts WGS84 coordinates to XYZ coordinates.

    :param lat: Latitude.
    :param lon: Longitude.
    :param zoom: Z coordinate.
    :return: The X and Y coordinates.
    """
    lat_rad = math.radians(lat)
    scale = 1 << zoom
    x = (lon + 180.0) / 360.0 * scale
    y = (1.0 - math.asinh(math.tan(lat_rad)) / math.pi) / 2.0 * scale
    return int(x), int(y)


def tile_coord_to_wgs84(x: float, y: float, zoom: int) -> Tuple[float, float]:
    """
    Converts XYZ tile coordinates to WGS84 coordinates.

    :param x: X coordinate.
    :param y: Y coordinate.
    :param zoom: Z coordinate.
    :return: WGS84 coordinates.
    """
    scale = 1 << zoom
    lon_deg = x / scale * 360.0 - 180.0
    lat_rad = math.atan(math.sinh(math.pi * (1 - 2 * y / scale)))
    lat_deg = math.degrees(lat_rad)
    return lat_deg, lon_deg


def convert_altitude(raw_altitude: int, lat: float, lon: float, tile_x: int, tile_y: int) -> Tuple[float, float]:
    """
    Converts the raw altitude returned by the API to height above MSL.

    :param raw_altitude: Raw altitude from the API.
    :param lat: WGS84 latitude of the location.
    :param lon: WGS84 longitude of the location.
    :param tile_x: X coordinate of the XYZ tile coordinates.
    :param tile_y: Y coordinate of the XYZ tile coordinates.
    :return: Height above MSL in meters.
    """
    # Adapted from _GEOOrientedPositionFromPDTilePosition in GeoServices.
    # Don't really have much of a clue what's going on here, but it seems to work
    zoom = 17
    top_left = tile_coord_to_mercator(tile_x, tile_y, zoom)
    top_right = tile_coord_to_mercator(tile_x + 1, tile_y, zoom)
    
    top_left_ecef = tf_web_mercator_to_ecef.transform(*top_left)
    top_right_ecef = tf_web_mercator_to_ecef.transform(*top_right)

    delta_x = top_left_ecef[0] - top_right_ecef[0]
    delta_y = top_left_ecef[1] - top_right_ecef[1]
    
    altitude = math.sqrt(delta_x**2 + delta_y**2) * (raw_altitude / 16383.0)
    geoid_height = get_geoid_height(lat, lon)
    elevation = altitude - geoid_height
    return altitude, elevation


def tile_coord_to_mercator(tile_x: int, tile_y: int, zoom: int) -> Tuple[float, float]:
    """
    Converts XYZ tile coordinates to Web Mercator coordinates.

    :param tile_x: X coordinate.
    :param tile_y: Y coordinate.
    :param zoom: Z coordinate.
    :return: The Web Mercator coordinate.
    """
    # Adapted from _GEOOrientedPositionFromPDTilePosition in GeoServices.
    # Don't really have much of a clue what's going on here, but it seems to work
    scale = 1 << zoom
    scale_recip = 1.0 / scale
    web_mercator_size = 40086474.44
    x = (tile_x * scale_recip - 0.5) * web_mercator_size
    y = ((scale + ~tile_y) * scale_recip - 0.5) * web_mercator_size
    return x, y


def get_geoid_height(lat: float, lon: float) -> float:
    """
    Returns the EGM2008 geoid height at a WGS84 coordinate.

    :param lat: Latitude.
    :param lon: Longitude.
    :return: Geoid height in meters.
    """
    _, _, geoid_height = tf_wgs84_to_wgs84_egm2008.transform(lat, lon, 0)
    return -geoid_height


def convert_pano_orientation(lat: float, lon: float, raw_yaw: int, raw_pitch: int, raw_roll: int) \
        -> Tuple[float, float, float]:
    """
    Converts the raw yaw/pitch/roll of a panorama returned by the API to the
    rotation to apply to the photosphere.

    :param lat: Latitude of the panorama.
    :param lon: Longitude of the panorama.
    :param altitude: GPS altitude (not height above MSL) of the panorama.
    :param raw_yaw: Raw yaw value from the API.
    :param raw_pitch: Raw pitch value from the API.
    :param raw_roll: Raw roll value from the API.
    :return: Converted heading/pitch/roll angles in radians.
    """
    yaw = (raw_yaw / 16383.0) * math.tau
    pitch = (raw_pitch / 16383.0) * math.tau
    roll = (raw_roll / 16383.0) * math.tau

    rot = Rotation.from_euler("xyz", (yaw, pitch, roll))
    rot *= Rotation.from_quat((0.5, 0.5, -0.5, -0.5))
    quat = rot.as_quat()
    quat2 = quat[3], -quat[2], -quat[0], quat[1]
    conv_roll, conv_pitch, conv_yaw = \
        Rotation.from_euler("xyz", 
                            _from_rigid_transform_ecef_no_offset(lat, lon, quat2))\
                .as_euler("zyx")
    return conv_yaw, conv_pitch, conv_roll


def _from_rigid_transform_ecef_no_offset(lat: float, lon: float,
                                         rotation: Tuple[float, float, float, float]) -> Tuple[float, float, float]:
    """
    via gdc::CameraFrame<>::fromRigidTransformEcefNoOffset() in VectorKit.
    I optimized out the ECEF coords, but I've decided to keep the name
    """
    ecef_basis = _create_local_ecef_basis(lat, lon)
    mult = Rotation.from_matrix(ecef_basis) * Rotation.from_quat(rotation)
    local_rot = mult.as_euler("zxy")
    return local_rot[2], -local_rot[1], -local_rot[0]


def _create_local_ecef_basis(lat: float, lon: float) -> np.ndarray:
    """
    via gdc::CameraFrame<>::createLocalEcefBasis() in VectorKit
    """
    lat = np.radians(lat)
    lon = np.radians(lon)
    cos_lat = np.cos(lat)
    sin_lat = np.sin(lat)
    cos_lon = np.cos(lon)
    sin_lon = np.sin(lon)

    ecef_basis = np.array([
        [-sin_lon, cos_lon, 0],
        [cos_lon * cos_lat, sin_lon * cos_lat, sin_lat],
        [cos_lon * sin_lat, sin_lon * sin_lat, -cos_lat]
    ])
    return ecef_basis
