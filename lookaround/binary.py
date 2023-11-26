import io
import struct
from typing import List


class BinaryReader:
    @property
    def stream(self) -> io.BytesIO:
        return self.bs

    def __init__(self, base_stream: io.BytesIO):
        self.bs = base_stream

    def read(self, size: int) -> bytes:
        return self.bs.read(size)

    def read_sbyte(self) -> int:
        return int.from_bytes(self.bs.read(1), byteorder="little", signed=True)

    def read_byte(self) -> int:
        return int.from_bytes(self.bs.read(1), byteorder="little", signed=False)

    def read_int2(self) -> int:
        return int.from_bytes(self.bs.read(2), byteorder="little", signed=True)

    def read_uint2(self) -> int:
        return int.from_bytes(self.bs.read(2), byteorder="little", signed=False)

    def read_int2_be(self) -> int:
        return int.from_bytes(self.bs.read(2), byteorder="big", signed=True)

    def read_uint2_be(self) -> int:
        return int.from_bytes(self.bs.read(2), byteorder="big", signed=False)

    def read_int4(self) -> int:
        return int.from_bytes(self.bs.read(4), byteorder="little", signed=True)

    def read_uint4(self) -> int:
        return int.from_bytes(self.bs.read(4), byteorder="little", signed=False)

    def read_int4_be(self) -> int:
        return int.from_bytes(self.bs.read(4), byteorder="big", signed=True)

    def read_uint4_be(self) -> int:
        return int.from_bytes(self.bs.read(4), byteorder="big", signed=False)

    def read_float(self) -> float:
        return struct.unpack("f", self.bs.read(4))[0]

    def read_floats(self, n: int) -> List[float]:
        return list(struct.unpack(f"{n}f", self.bs.read(n * 4)))

    def read_double(self) -> float:
        return struct.unpack("d", self.bs.read(8))[0]

    def read_doubles(self, n: int) -> List[float]:
        return list(struct.unpack(f"{n}d", self.bs.read(n * 8)))


class BinaryWriter:
    @property
    def stream(self) -> io.BytesIO:
        return self.bs

    @property
    def content(self) -> bytes:
        return self.bs.getvalue()

    def __init__(self, base_stream: io.BytesIO):
        self.bs = base_stream

    def write(self, b: bytes):
        self.bs.write(b)

    def write_sbyte(self, n: int):
        self.bs.write(struct.pack("b", n))

    def write_byte(self, n: int):
        self.bs.write(struct.pack("B", n))

    def write_int2(self, n: int):
        self.bs.write(struct.pack("h", n))

    def write_uint2(self, n: int):
        self.bs.write(struct.pack("H", n))

    def write_int2_be(self, n: int):
        self.bs.write(struct.pack(">h", n))

    def write_uint2_be(self, n: int):
        self.bs.write(struct.pack(">H", n))

    def write_int4(self, n: int):
        self.bs.write(struct.pack("i", n))

    def write_uint4(self, n: int):
        self.bs.write(struct.pack("I", n))

    def write_int4_be(self, n: int):
        self.bs.write(struct.pack(">i", n))

    def write_uint4_be(self, n: int):
        self.bs.write(struct.pack(">I", n))
