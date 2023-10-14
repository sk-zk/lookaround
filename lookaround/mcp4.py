import io
from dataclasses import dataclass
from typing import List


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
    entries_count = int.from_bytes(stream.read(2), byteorder="little")

    entries = []
    for i in range(0, entries_count):
        datatype = int.from_bytes(stream.read(2), byteorder="little")
        offset = int.from_bytes(stream.read(4), byteorder="little")
        length = int.from_bytes(stream.read(4), byteorder="little")

        stream_pos = stream.tell()
        stream.seek(offset)
        content = stream.read(length)
        stream.seek(stream_pos)

        entries.append(MCP4Entry(datatype, content))

    return entries
