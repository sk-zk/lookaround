import io
import struct
from dataclasses import dataclass
from typing import List, Union, Tuple
from enum import Enum

import liblzfse

from .binary import BinaryReader

MCP4_MAGIC = b"MCP4"


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
    magic = r.read(4)
    if magic != MCP4_MAGIC:
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

    print(compression_method)
    if compression_method == CompressionMethod.LZFSE:
        # first four bytes are length of decompressed entry, we can just ignore that
        content = liblzfse.decompress(content[4:])
    elif compression_method != CompressionMethod.NONE:
        raise NotImplementedError()

    return content


def pack(entries: List[MCP4Entry]) -> bytes:
    stream = io.BytesIO()

    # write file header
    stream.write(MCP4_MAGIC)
    stream.write(struct.pack("H", 0))
    stream.write(struct.pack("H", len(entries)))

    # compress and pack entries
    entry_bytes = []
    for entry in entries:
        if entry.type == EntryType.MESH_DATA:
            content = struct.pack("I", len(entry.content)) + liblzfse.compress(entry.content)
            compression_method = CompressionMethod.LZFSE.value
        else:
            content = entry.content
            compression_method = CompressionMethod.NONE.value
        entry_bytes.append(struct.pack("b", compression_method) + content)

    # write entry offsets
    header_length = stream.tell() + ((2+4+4) * len(entries))
    offset = header_length
    for i in range(0, len(entries)):
        stream.write(struct.pack("H", entries[i].type.value))
        stream.write(struct.pack("I", offset))
        stream.write(struct.pack("I", len(entry_bytes[i])))
        offset += len(entry_bytes[i])

    # write entries
    for entry in entry_bytes:
        stream.write(entry)

    return stream.getvalue()


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


def parse_connectivity_chunk(connectivity_bytes: bytes):
    r = BinaryReader(io.BytesIO(connectivity_bytes))
    num_symbols = r.read_uint4()
    _ = r.read_uint4()
    _ = r.read_uint4()
    _ = r.read_uint4()
    _ = r.read_uint4()
    _ = r.read_uint4()
    clers_string = r.read(num_symbols).decode("ascii")
    return clers_string


@dataclass
class VerticesCamChunk:
    vertex_count: int
    unknown_vec: List[float]
    unknown1: int
    cam_matrix_maybe: List[float]
    unknown2: int
    rotation: List[float]
    unknown3: int
    compressed_vertices: bytes
    other_stuff: bytes


def parse_vertices_cam_chunk(vertices_cam_bytes: bytes) -> VerticesCamChunk:
    r = BinaryReader(io.BytesIO(vertices_cam_bytes))
    vertex_count = r.read_uint4()
    unknown_vec = r.read_floats(3)
    unknown1 = r.read_int2()
    cam_matrix_maybe = r.read_doubles(16)
    unknown2 = r.read_int4()
    rotation = r.read_doubles(4)
    unknown3 = r.read_int4()
    compressed_vertices = r.read(vertex_count * 3)
    other_stuff = r.stream.read()
    return VerticesCamChunk(vertex_count,
                            unknown_vec,
                            unknown1,
                            cam_matrix_maybe,
                            unknown2,
                            rotation,
                            unknown3,
                            compressed_vertices,
                            other_stuff)


def pack_vertices_cam_chunk(vcc: VerticesCamChunk) -> bytes:
    stream = io.BytesIO()
    stream.write(struct.pack("I", vcc.vertex_count))
    stream.write(struct.pack("fff", *vcc.unknown_vec))
    stream.write(struct.pack("h", vcc.unknown1))
    stream.write(struct.pack("dddddddddddddddd", *vcc.cam_matrix_maybe))
    stream.write(struct.pack("i", vcc.unknown2))
    stream.write(struct.pack("dddd", *vcc.rotation))
    stream.write(struct.pack("i", vcc.unknown3))
    stream.write(vcc.compressed_vertices)
    stream.write(vcc.other_stuff)
    return stream.getvalue()
