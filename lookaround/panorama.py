from dataclasses import dataclass
from datetime import datetime
from typing import Any


@dataclass
class LookaroundPanorama:
    panoid: int
    build_id: int
    lat: float 
    lon: float 
    heading: float = None
    camera_metadata: Any = None
    elevation: float = None
    coverage_type: int = None
    timestamp: int = None
    has_blurs: bool = None

    @property
    def date(self):
        return datetime.fromtimestamp(int(self.timestamp) / 1000.0)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.panoid}/{self.build_id} ({self.lat:.6}, {self.lon:.6}) " \
               f"[{self.date.strftime('%Y-%m-%d')}]"
