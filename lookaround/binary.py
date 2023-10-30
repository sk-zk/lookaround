import io


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

    def read_int4(self) -> int:
        return int.from_bytes(self.bs.read(4), byteorder="little", signed=True)

    def read_uint4(self) -> int:
        return int.from_bytes(self.bs.read(4), byteorder="little", signed=False)
