In which I attempt to reverse engineer Apple Look Around.

## Coverage tiles
Panoramas can be found as XYZ tiles with z=17. I've abstracted this a bit for convenience:

```python
from lookaround import get_coverage_tile_by_latlon

# fetches all panoramas on the tile which contains this coordinate
panos = get_coverage_tile_by_latlon(49.49277003930681, 6.588420315065048)
print(len(panos))
print(panos[0].panoid)
print(panos[0].region_id)  # not sure what this actually is, but it's
                           # required for downloading images, and it's the same for
                           # each pano on a tile, for many tiles within a region,
                           # so "region_id" it is
print(panos[0].lat, panos[0].lon)
print(panos[0].date)
```

## Authentication
Requests for the actual image data must be authenticated.
The code for this is a translation of [retroplasma/flyover-reverse-engineering](https://github.com/retroplasma/flyover-reverse-engineering) (without which
none of this would've been possible).

```python
from lookaround.auth import Authenticator

auth = Authenticator()
# example:
url = auth.authenticate_url("https://gspe72-ssl.ls.apple.com/mnn_us/0665/1337/7609/6445/9400/1095101453/t/0/2")
```

## Downloading imagery
Now that we can find panoramas and authenticate our download requests, let's go download one.
I don't know how to stitch these together yet (or if you'd even need to) because it's not quite as straightforward as it is with Street View, but
we can at the very least look at the raw images.

```python
from lookaround import get_coverage_tile_by_latlon, fetch_pano_segment
from lookaround.auth import Authenticator

panos = get_coverage_tile_by_latlon(49.49277003930681, 6.588420315065048)
auth = Authenticator()
zoom = 2 # resolution / zoom level. 0 is highest, 7 is lowest.
for segment in range(0, 6): # segment to download. 0-3 are the sides, 4 is up, 5 is down.
    image = fetch_pano_segment(panos[0].panoid, panos[0].region_id, segment, zoom, auth)
    with open(f"{panos[0].panoid}_{segment}_{zoom}.heic", "wb") as f:
        f.write(image)
```

Images are returned as HEIC, so you may need to install some plugins to view them.
