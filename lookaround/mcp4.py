import io
from dataclasses import dataclass
from typing import List, Union, Tuple
from enum import Enum

import liblzfse

from .binary import BinaryReader


class EntryType(Enum):
    UNKNOWN0 = 0
    MESH_DATA = 1
    UNKNOWN2 = 2
    HEIC = 3
    UNKNOWN5 = 5


class CompressionMethod(Enum):
    NONE = 0
    LZMA = 2
    LZFSE = 3


class MeshChunkType(Enum):
    UNKNOWN0 = 0
    VI_CONNECTIVITY_EB = 4
    MATERIAL_ID = 5
    VERTICES_PREDICTIVE = 6
    UV_PREDICTIVE = 7
    VERTICES_CUBE = 8
    VERTICES_CAM = 9
    UV_MODEL = 10
    POSTPROCESS = 11


@dataclass
class MeshChunk:
    type: MeshChunkType
    content: bytes


@dataclass
class MCP4Entry:
    type: EntryType
    content: bytes


def parse(mcp4_bytes: bytes) -> List[MCP4Entry]:
    r = BinaryReader(io.BytesIO(mcp4_bytes))
    magic = r.read(4).decode("ascii")
    if magic != "MCP4":
        raise ValueError("Not a MCP4 file")

    _ = r.read_int2()  # unknown purpose
    entries_count = r.read_uint2()

    entries = []
    for i in range(0, entries_count):
        entry_type = EntryType(r.read_uint2())
        offset = r.read_uint4()
        length = r.read_uint4()

        content = extract_entry(length, offset, r)
        entry = MCP4Entry(entry_type, content)
        entries.append(entry)

    return entries


def extract_entry(length: int, offset: int, r: BinaryReader) -> bytes:
    # _mc_container_get_chapter_data in VectorKit
    stream_pos = r.stream.tell()
    r.stream.seek(offset)
    compression_method = CompressionMethod(r.read_byte())
    content = r.read(length - 1)
    r.stream.seek(stream_pos)

    if compression_method == CompressionMethod.LZFSE:
        content = liblzfse.decompress(content[4:])
    elif compression_method != CompressionMethod.NONE:
        raise NotImplementedError()

    return content


def parse_mesh_chunks(chunks_bytes: bytes) -> List[MeshChunk]:
    # _mc_mesh_decode in VectorKit
    r = BinaryReader(io.BytesIO(chunks_bytes))

    chunks = []
    while r.stream.tell() < len(chunks_bytes):
        chunk_type, length = parse_mesh_chunk_header(r)
        content = r.read(length)
        chunks.append(MeshChunk(chunk_type, content))
    return chunks


def parse_mesh_chunk_header(r: BinaryReader) -> Tuple[MeshChunkType, int]:
    magic = r.read(4).decode("ascii")
    if magic != "CHNK":
        raise ValueError("Invalid mesh data")
    _ = r.read_uint2()  # always 1?
    chunk_type = MeshChunkType(r.read_uint4())
    _ = r.read_uint4()  # always 1?
    length = r.read_uint4()
    _ = r.read_uint4()  # always 0?
    return chunk_type, length
