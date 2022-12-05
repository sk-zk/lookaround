class LookaroundPanorama:
    def __init__(self, panoid, region_id, lat, lon, heading, projection):
        self.panoid = panoid
        self.region_id = region_id
        self.lat = lat
        self.lon = lon
        self.heading = heading
        self.projection = projection

        self.raw_elevation = None
        self.coverage_type = None
        self.date = None

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"{self.panoid}/{self.region_id} ({self.lat:.6}, {self.lon:.6}) " \
               f"[{self.date.strftime('%Y-%m-%d')}]"
