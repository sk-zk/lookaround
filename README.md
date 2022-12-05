In which I reverse-engineer Apple Look Around and create a Python module for it.

## Recent breaking changes
* `LookaroundPanorama.north` has been renamed to `LookaroundPanorama.heading`.

## Coverage tiles
Panoramas can be found as XYZ tiles with z=17. I've abstracted this a bit for convenience:

```python
from lookaround import get_coverage_tile_by_latlon

# fetches all panoramas on the tile which contains this coordinate
panos = get_coverage_tile_by_latlon(49.49277003930681, 6.588420315065048)
print(len(panos))
print(panos[0].panoid)
print(panos[0].region_id)  # I have no idea what this actually is, but it's
                           # a secondary key required for downloading images
                           # which appears to stay the same for a large region,
                           # so I'm calling it a region_id for now.
                           # Could be a camera ID as well.
print(panos[0].lat, panos[0].lon)
print(panos[0].date)
```

Alternatively, if you've got tile coordinates already, you can call `get_coverage_tile` instead.

## Authentication
Requests for the actual image data and some (but not all) map tile types must be authenticated dynamically.
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

Panoramas are made of six faces; four side faces (0-3) and a top (4) and bottom (5) face.
Each face can be downloaded in eight different resolutions, where 0 is the largest and 7 is the smallest.

```python
from lookaround import get_coverage_tile_by_latlon, get_pano_face
from lookaround.auth import Authenticator

panos = get_coverage_tile_by_latlon(49.49277003930681, 6.588420315065048)
auth = Authenticator()
zoom = 2
for face in range(0, 6):
    image = get_pano_face(panos[0].panoid, panos[0].region_id, face, zoom, auth)
    with open(f"{panos[0].panoid}_{face}_{zoom}.heic", "wb") as f:
        f.write(image)
```

The side faces are equirectangular and can be stitched together easily, but the other two use a different projection
which I'm struggling to deal with.

Images are in HEIC format, so you may need to install some plugins to view them.
