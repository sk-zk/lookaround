# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: MapTile.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rMapTile.proto\x12\x0bstreetlevel\"\xc4\n\n\x07MapTile\x12\'\n\x04pano\x18\x01 \x03(\x0b\x32\x19.streetlevel.MapTile.Pano\x12\x31\n\tunknown13\x18\x04 \x03(\x0b\x32\x1e.streetlevel.MapTile.Unknown13\x12\x33\n\nprojection\x18\x05 \x03(\x0b\x32\x1f.streetlevel.MapTile.Projection\x12<\n\x0ftile_coordinate\x18\x06 \x01(\x0b\x32#.streetlevel.MapTile.TileCoordinate\x1a\xf5\x02\n\x04Pano\x12\x0e\n\x06panoid\x18\x01 \x01(\x04\x12\x10\n\x08unknown1\x18\x04 \x01(\x05\x12\x11\n\ttimestamp\x18\x05 \x01(\x03\x12\x15\n\rregion_id_idx\x18\x07 \x01(\x05\x12\x10\n\x08unknown3\x18\t \x03(\x05\x12\x34\n\x08location\x18\n \x01(\x0b\x32\".streetlevel.MapTile.Pano.Location\x12\x34\n\x08unknown5\x18\x0c \x01(\x0b\x32\".streetlevel.MapTile.Pano.Unknown5\x1a\x83\x01\n\x08Location\x12\x18\n\x10longitude_offset\x18\x01 \x01(\x05\x12\x17\n\x0flatitude_offset\x18\x02 \x01(\x05\x12\x10\n\x08unknown8\x18\x03 \x01(\x05\x12\x10\n\x08unknown9\x18\x04 \x01(\x05\x12\x0f\n\x07north_x\x18\x05 \x01(\x05\x12\x0f\n\x07north_y\x18\x06 \x01(\x05\x1a\x1d\n\x08Unknown5\x12\x11\n\tunknown12\x18\x01 \x03(\x05\x1a\xb6\x01\n\tUnknown13\x12\x11\n\tunknown14\x18\x01 \x01(\x05\x12\x11\n\tregion_id\x18\x03 \x01(\x05\x12\x11\n\tunknown15\x18\x04 \x01(\x05\x12\x11\n\tunknown16\x18\x05 \x01(\x05\x12\x11\n\tunknown17\x18\x06 \x01(\x05\x12\x11\n\tunknown18\x18\t \x01(\x05\x12\x11\n\tunknown19\x18\n \x01(\x05\x12\x11\n\tunknown20\x18\x0b \x01(\x05\x12\x11\n\tunknown21\x18\x0c \x01(\x05\x1a\x85\x04\n\nProjection\x12\x0c\n\x04\x66\x61\x63\x65\x18\x01 \x01(\x05\x12<\n\tunknown24\x18\x04 \x01(\x0b\x32).streetlevel.MapTile.Projection.Unknown24\x12<\n\tunknown25\x18\x05 \x01(\x0b\x32).streetlevel.MapTile.Projection.Unknown25\x12\x11\n\tunknown26\x18\x06 \x01(\x05\x1a\xd2\x01\n\tUnknown24\x12\x11\n\tunknown27\x18\x01 \x01(\x05\x12\x16\n\x0elongitude_size\x18\x02 \x01(\x01\x12\x15\n\rlatitude_size\x18\x03 \x01(\x01\x12\x11\n\tunknown30\x18\x04 \x01(\x01\x12\x11\n\tunknown31\x18\x05 \x01(\x01\x12\x11\n\tunknown32\x18\x06 \x01(\x01\x12\x11\n\tunknown33\x18\x07 \x01(\x01\x12\x11\n\tunknown34\x18\x08 \x01(\x01\x12\x11\n\tunknown35\x18\t \x01(\x01\x12\x11\n\tunknown36\x18\n \x01(\x01\x1a\x84\x01\n\tUnknown25\x12\x11\n\tunknown37\x18\x01 \x01(\x01\x12\x11\n\tunknown38\x18\x02 \x01(\x01\x12\x11\n\tunknown39\x18\x03 \x01(\x01\x12\x18\n\x10longitude_center\x18\x04 \x01(\x01\x12\x11\n\tunknown41\x18\x05 \x01(\x01\x12\x11\n\tunknown42\x18\x06 \x01(\x01\x1a\x31\n\x0eTileCoordinate\x12\t\n\x01x\x18\x01 \x01(\x05\x12\t\n\x01y\x18\x02 \x01(\x05\x12\t\n\x01z\x18\x03 \x01(\x05\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'MapTile_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _MAPTILE._serialized_start=31
  _MAPTILE._serialized_end=1379
  _MAPTILE_PANO._serialized_start=250
  _MAPTILE_PANO._serialized_end=623
  _MAPTILE_PANO_LOCATION._serialized_start=461
  _MAPTILE_PANO_LOCATION._serialized_end=592
  _MAPTILE_PANO_UNKNOWN5._serialized_start=594
  _MAPTILE_PANO_UNKNOWN5._serialized_end=623
  _MAPTILE_UNKNOWN13._serialized_start=626
  _MAPTILE_UNKNOWN13._serialized_end=808
  _MAPTILE_PROJECTION._serialized_start=811
  _MAPTILE_PROJECTION._serialized_end=1328
  _MAPTILE_PROJECTION_UNKNOWN24._serialized_start=983
  _MAPTILE_PROJECTION_UNKNOWN24._serialized_end=1193
  _MAPTILE_PROJECTION_UNKNOWN25._serialized_start=1196
  _MAPTILE_PROJECTION_UNKNOWN25._serialized_end=1328
  _MAPTILE_TILECOORDINATE._serialized_start=1330
  _MAPTILE_TILECOORDINATE._serialized_end=1379
# @@protoc_insertion_point(module_scope)
