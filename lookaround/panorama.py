from dataclasses import dataclass
from datetime import datetime
from typing import Any, Tuple

from . import geo


@dataclass
class LookaroundPanorama:
    panoid: int
    build_id: int
    lat: float 
    lon: float
    camera_metadata: Any = None
    coverage_type: int = None
    timestamp: int = None
    has_blurs: bool = None
    raw_orientation: Tuple[int, int, int] = None
    raw_altitude: int = None
    tile: Tuple[int, int, int] = None

    _heading: float = None
    _elevation: float = None
    _altitude: float = None

    def _set_altitude_and_elevation(self):
        if not self._elevation:
            self._altitude, self._elevation = \
                geo.convert_altitude(self.raw_altitude, self.lat, self.lon, self.tile[0], self.tile[1])

    @property
    def elevation(self):
        self._set_altitude_and_elevation()
        return self._elevation

    @property
    def heading(self):
        if not self._heading:
            self._set_altitude_and_elevation()
            self._heading, _, _ = geo.convert_pano_orientation(self.lat, self.lon, self._altitude,
                                                               *self.raw_orientation)
        return self._heading

    @property
    def date(self):
        return datetime.fromtimestamp(int(self.timestamp) / 1000.0)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.panoid}/{self.build_id} ({self.lat:.6}, {self.lon:.6}) " \
               f"[{self.date.strftime('%Y-%m-%d')}]"
