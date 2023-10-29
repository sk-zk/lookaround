import io
from dataclasses import dataclass
from typing import List
import struct
from enum import Enum

import liblzfse


class CompressionMethod(Enum):
    NONE = 0
    LZMA = 2
    LZFSE = 3


@dataclass
class MCP4Entry:
    type: int
    content: bytes


def parse(mcp4_bytes: bytes) -> List[MCP4Entry]:
    stream = io.BytesIO(mcp4_bytes)
    magic = stream.read(4).decode("ascii")
    if magic != "MCP4":
        raise ValueError("Not a MCP4 file")

    _ = stream.read(2)  # unknown purpose
    entries_count = struct.unpack("H", stream.read(2))[0]

    entries = []
    for i in range(0, entries_count):
        datatype = struct.unpack("h", stream.read(2))[0]
        offset = struct.unpack("i", stream.read(4))[0]
        length = struct.unpack("i", stream.read(4))[0]

        content = extract_entry(length, offset, stream)
        entry = MCP4Entry(datatype, content)
        entries.append(entry)

    return entries


def extract_entry(length: int, offset: int, stream: io.BytesIO) -> bytes:
    # _mc_container_get_chapter_data in VectorKit
    stream_pos = stream.tell()
    stream.seek(offset)
    compression_method = CompressionMethod(struct.unpack("b", stream.read(1))[0])
    content = stream.read(length - 1)
    stream.seek(stream_pos)

    if compression_method == CompressionMethod.LZFSE:
        content = liblzfse.decompress(content[4:])
    elif compression_method != CompressionMethod.NONE:
        raise NotImplementedError()

    return content
