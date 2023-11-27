# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Shared.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cShared.proto\x12\x0bstreetlevel\"\"\n\x06LatLng\x12\x0b\n\x03lat\x18\x01 \x01(\x01\x12\x0b\n\x03lng\x18\x02 \x01(\x01*\xe1\x01\n\x0eMapsResultType\x12\x1c\n\x18MAPS_RESULT_TYPE_UNKNOWN\x10\x00\x12\x1a\n\x16MAPS_RESULT_TYPE_PLACE\x10\x01\x12\x1f\n\x1bMAPS_RESULT_TYPE_COLLECTION\x10\x02\x12\x1e\n\x1aMAPS_RESULT_TYPE_PUBLISHER\x10\x03\x12(\n$MAPS_RESULT_TYPE_PLACE_QUESTIONNAIRE\x10\x04\x12*\n&MAPS_RESULT_TYPE_BATCH_REVERSE_GEOCODE\x10\x05*\xb2\x12\n\x0bRequestType\x12\x18\n\x14REQUEST_TYPE_UNKNOWN\x10\x00\x12\x17\n\x13REQUEST_TYPE_SEARCH\x10\x01\x12\x1a\n\x16REQUEST_TYPE_GEOCODING\x10\x02\x12*\n&REQUEST_TYPE_CANONICAL_LOCATION_SEARCH\x10\x03\x12\"\n\x1eREQUEST_TYPE_REVERSE_GEOCODING\x10\x04\x12\x1d\n\x19REQUEST_TYPE_PLACE_LOOKUP\x10\x05\x12 \n\x1cREQUEST_TYPE_MERCHANT_LOOKUP\x10\x06\x12!\n\x1dREQUEST_TYPE_PLACE_REFINEMENT\x10\x07\x12\x1c\n\x18REQUEST_TYPE_SIRI_SEARCH\x10\x08\x12)\n%REQUEST_TYPE_LOCATION_DIRECTED_SEARCH\x10\t\x12\x1d\n\x19REQUEST_TYPE_AUTOCOMPLETE\x10\n\x12+\n\'REQUEST_TYPE_BROWSE_CATEGORY_SUGGESTION\x10\x0b\x12 \n\x1cREQUEST_TYPE_CATEGORY_SEARCH\x10\x0c\x12\x1f\n\x1bREQUEST_TYPE_POPULAR_NEARBY\x10\r\x12\x31\n-REQUEST_TYPE_ZERO_KEYWORD_CATEGORY_SUGGESTION\x10\x0e\x12)\n%REQUEST_TYPE_SEARCH_FIELD_PLACEHOLDER\x10\x0f\x12,\n(REQUEST_TYPE_BATCH_POPULAR_NEARBY_SEARCH\x10\x10\x12\x31\n-REQUEST_TYPE_VENDOR_SPECIFIC_PLACE_REFINEMENT\x10\x11\x12\x1e\n\x1aREQUEST_TYPE_NEARBY_SEARCH\x10\x12\x12)\n%REQUEST_TYPE_ADDRESS_OBJECT_GEOCODING\x10\x13\x12<\n8REQUEST_TYPE_ZERO_KEYWORD_WITH_SEARCH_RESULTS_SUGGESTION\x10\x14\x12(\n$REQUEST_TYPE_EXTERNAL_TRANSIT_LOOKUP\x10\x15\x12%\n!REQUEST_TYPE_FEATURE_ID_GEOCODING\x10\x16\x12-\n)REQUEST_TYPE_MAPS_IDENTIFIER_PLACE_LOOKUP\x10\x17\x12%\n!REQUEST_TYPE_DATASET_STATUS_CHECK\x10\x18\x12$\n REQUEST_TYPE_OFFLINE_AREA_LOOKUP\x10\x19\x12(\n$REQUEST_TYPE_BATCH_REVERSE_GEOCODING\x10\x1a\x12*\n&REQUEST_TYPE_OFFLINE_SUGGESTED_REGIONS\x10\x1b\x12+\n\'REQUEST_TYPE_OFFLINE_POLYGON_QUAD_NODES\x10\x1c\x12*\n&REQUEST_TYPE_OFFLINE_PROACTIVE_REGIONS\x10\x1d\x12\x1d\n\x19REQUEST_TYPE_BRAND_LOOKUP\x10\x1e\x12(\n$REQUEST_TYPE_OFFLINE_UPDATE_MANIFEST\x10\x1f\x12(\n$REQUEST_TYPE_WIFI_FINGERPRINT_LOOKUP\x10 \x12+\n\'REQUEST_TYPE_INITIAL_OFFLINE_SUGGESTION\x10!\x12\x1e\n\x1aREQUEST_TYPE_IP_GEO_LOOKUP\x10\"\x12\"\n\x1eREQUEST_TYPE_GROUND_VIEW_LABEL\x10#\x12%\n!REQUEST_TYPE_BATCH_SPATIAL_LOOKUP\x10$\x12)\n%REQUEST_TYPE_TRANSIT_VEHICLE_POSITION\x10%\x12(\n$REQUEST_TYPE_PLACE_COLLECTION_LOOKUP\x10&\x12(\n$REQUEST_TYPE_TRANSIT_SCHEDULE_LOOKUP\x10\'\x12&\n\"REQUEST_TYPE_BATCH_CATEGORY_LOOKUP\x10(\x12,\n(REQUEST_TYPE_BATCH_MERCHANT_LOOKUP_BRAND\x10)\x12/\n+REQUEST_TYPE_CHILD_PLACE_LOOKUP_BY_CATEGORY\x10*\x12&\n\"REQUEST_TYPE_COLLECTION_SUGGESTION\x10+\x12!\n\x1dREQUEST_TYPE_MAPS_SEARCH_HOME\x10,\x12+\n\'REQUEST_TYPE_PLACE_QUESTIONNAIRE_LOOKUP\x10-\x12\x1f\n\x1bREQUEST_TYPE_PUBLISHER_VIEW\x10.\x12%\n!REQUEST_TYPE_ALL_COLLECTIONS_VIEW\x10/\x12,\n(REQUEST_TYPE_AIRPORT_ENTITY_PLACE_LOOKUP\x10\x30\x12!\n\x1dREQUEST_TYPE_TERRITORY_LOOKUP\x10\x31\x12/\n+REQUEST_TYPE_TRANSIT_NEARBY_SCHEDULE_LOOKUP\x10\x32\x12\x1a\n\x16REQUEST_TYPE_MAPS_HOME\x10\x33\x12%\n!REQUEST_TYPE_ALL_GUIDES_LOCATIONS\x10\x34\x12\x1c\n\x18REQUEST_TYPE_GUIDES_HOME\x10\x35\x12$\n REQUEST_TYPE_EXTENDED_GEO_LOOKUP\x10\x36\x12$\n REQUEST_TYPE_QUERY_UNDERSTANDING\x10\x37\x12&\n\"REQUEST_TYPE_POI_AT_ADDRESS_LOOKUP\x10\x38\x12\x35\n1REQUEST_TYPE_TRANSIT_NEARBY_PAYMENT_METHOD_LOOKUP\x10\x39\x12%\n!REQUEST_TYPE_PLACECARD_ENRICHMENT\x10:b\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'Shared_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_MAPSRESULTTYPE']._serialized_start=66
  _globals['_MAPSRESULTTYPE']._serialized_end=291
  _globals['_REQUESTTYPE']._serialized_start=294
  _globals['_REQUESTTYPE']._serialized_end=2648
  _globals['_LATLNG']._serialized_start=29
  _globals['_LATLNG']._serialized_end=63
# @@protoc_insertion_point(module_scope)
