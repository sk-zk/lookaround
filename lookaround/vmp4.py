import io
import struct
from dataclasses import dataclass
from typing import List, Union, Tuple
from enum import Enum
import zlib

from .binary import BinaryReader

VMP4_MAGIC = b"VMP4"


class EntryType(Enum):
    GLOBAL = 1
    LABELS = 10
    LABEL_LANGUAGES = 0xb
    LABEL_LOCALIZATIONS_2 = 0xd
    VERTICES = 0x14
    POINT_FEATURES = 0x1e
    LINE_FEATURES = 0x1f
    POLYGON_FEATURES = 0x20
    BUILDING_FEATURES = 0x21
    COASTLINE_FEATURES = 0x22
    WRAPPING_COASTLINE_FEATURES = 0x26
    BUILDING_MESHES = 0x27
    LINE_POINT_CHARACTERISTICS = 0x33
    POLYGON_POINT_CHARACTERISTICS = 0x34
    POLYGON_POINT_LABEL_POSITIONS = 0x37
    CONNECTIVITY = 0x3c
    GEO_ID_SEGMENTS = 0x50
    ADDRESS_RANGES = 0x5a
    TILE_REFERENCES = 0x5d
    HIGH_RES_BUILDINGS = 0x60
    DEBUG_BLOB = 100
    ELEVATION_RASTER = 0x65
    STYLE_ATTRIBUTE_RASTER = 0x66
    DAVINCI_METADATA = 0x67
    LOW_RES_BUILDINGS = 0x68
    TRANSIT_MZR_OVERRIDE = 0x70
    COVERAGE = 0x77
    TRANSIT_SYSTEMS = 0x80
    TRANSIT_NETWORK = 0x81
    ROAD_NETWORK = 0x87
    VENUE_MZR_OVERRIDE = 0x88
    VENUES = 0x89
    STOREFRONTS = 0x8a
    LOW_RES_BORDER_BUILDINGS = 0x8b
    BORDER_BUILDING_MESHES = 0x8c
    LABEL_PLACEMENT_METADATA = 0x8d
    DA_VINCI_BUILDINGS = 0x8e
    POINT_FEATURES_ADDENDUM = 0x90
    LINES_EXTENDED = 0x91
    TRAFFIC_SKELETON_1 = 0x92
    DA_VINCI_LANDMARKS = 0x93
    LINE_WIDTHS_1 = 0x94
    POINT_LABEL_ANNOTATIONS = 0x95
    POI_MZR_OVERRIDES = 0x97
    TRAFFIC_SKELETON_2 = 0x98
    LINE_WIDTHS_2 = 0x99
    STYLE_ATTRIBUTE_RASTER_2 = 0x9a
    MATERIAL_RASTER = 0x9b


@dataclass
class VMP4Entry:
    type: EntryType
    content: bytes


def parse(vmp4_bytes: bytes) -> List[VMP4Entry]:
    r = BinaryReader(io.BytesIO(vmp4_bytes))
    magic = r.read(4)
    if magic != VMP4_MAGIC:
        raise ValueError("Not a VMP4 file")

    _ = r.read_uint2()

    entries_count = r.read_uint2()

    entries = []
    for i in range(0, entries_count):
        entry_type = EntryType(r.read_uint2())
        offset = r.read_uint4()
        length = r.read_uint4()

        stream_pos = r.stream.tell()
        r.stream.seek(offset)
        compressed = r.read_byte() == 1
        content = r.read(length - 1)
        if compressed:
            # first four bytes are an int with unknown purpose
            content = zlib.decompress(content[4:])
        r.stream.seek(stream_pos)

        entries.append(VMP4Entry(entry_type, content))

    return entries


def parse_labels_entry(entry_bytes: bytes) -> List[str]:
    labels = []
    last_null = -1
    for i in range(0, len(entry_bytes)):
        if entry_bytes[i] == 0:
            labels.append(entry_bytes[last_null+1:i].decode("utf-8"))
            last_null = i
    return labels
