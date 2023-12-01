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
    _pitch: float = None
    _roll: float = None
    _elevation: float = None
    _altitude: float = None

    def _set_altitude_and_elevation(self):
        if not self._elevation:
            self._altitude, self._elevation = \
                geo.convert_altitude(self.raw_altitude, self.lat, self.lon, self.tile[0], self.tile[1])
            
    def _set_orientation(self):
        if not self._heading:
            self._heading, self._pitch, self._roll = \
                geo.convert_pano_orientation(self.lat, self.lon, *self.raw_orientation)

    @property
    def elevation(self):
        self._set_altitude_and_elevation()
        return self._elevation

    @property
    def heading(self):
        self._set_orientation()
        return self._heading

    @property
    def pitch(self):
        self._set_orientation()
        return self._pitch
    
    @property
    def roll(self):
        self._set_orientation()
        return self._roll
    
    @property
    def date(self):
        return datetime.fromtimestamp(int(self.timestamp) / 1000.0)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.panoid}/{self.build_id} ({self.lat:.6}, {self.lon:.6}) " \
               f"[{self.date.strftime('%Y-%m-%d')}]"
