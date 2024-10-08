In which I reverse-engineer Apple Look Around and create a Python module for it.

The reasonably stable parts of this have been integrated into my library [sk-zk/streetlevel](https://github.com/sk-zk/streetlevel/), and the experimenting happens over here.

## Coverage tiles
Panoramas can be found as XYZ tiles with z=17. Here's how you can fetch a tile:

```python
import math
from lookaround import get_coverage_tile_by_latlon

# fetches all panoramas on the tile which contains this coordinate
tile = get_coverage_tile_by_latlon(46.529426, 10.455443)
first = tile.panos[0]

print(len(tile.panos))
print(first.panoid, first.build_id)
print(first.lat, first.lon)
print(math.degrees(first.heading))
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

Panoramas are made up of six faces; four side faces (0-3) and a top (4) and bottom (5) face.
Each face can be downloaded in eight different resolutions, where 0 is the largest and 7 is the smallest.

```python
from lookaround import get_coverage_tile_by_latlon, get_pano_face
from lookaround.auth import Authenticator

tile = get_coverage_tile_by_latlon(46.52943, 10.45544)
first = tile.panos[0]

auth = Authenticator()
zoom = 2
for face in range(0, 6):
    image = get_pano_face(first.panoid, first.build_id, face, zoom, auth)
    with open(f"{first.panoid}_{face}_{zoom}.heic", "wb") as f:
        f.write(image)
```

Images are in HEIC format, so you may need to install some plugins to view them. See [here](https://streetlevel.readthedocs.io/en/v0.6.5/streetlevel.lookaround.html)
for an explanation of how you can render these panoramas, and [here](https://github.com/sk-zk/lookaround-map/blob/main/js/viewer/LookaroundAdapter.js#L145)
for my code which builds a mesh in Three.js.

## m / mt
There are two additional files requested by the Apple Maps client, `/m/<zoom>` and `/mt/7`.
The response is a file in a custom binary format with the header `MCP4`, containing several binary blobs.
The `mt` file contains the mesh data, the pano faces at zoom level 7, and some other stuff.

Here's how you can fetch the `mt` file and dump its contents:

```python
import lookaround
from lookaround import mcp4
from lookaround.auth import Authenticator

auth = Authenticator()
pano_id, build_id = 10690709345221411827, 1596925660
entries = mcp4.parse(lookaround.get_mt7_file(pano_id, build_id, auth))

for i in range(len(entries)):
    filetype, content = entries[i].type, entries[i].content
    if filetype == mcp4.EntryType.HEIC:
        ext = "heic"
    elif filetype == mcp4.EntryType.MESH_DATA:
        ext = "mesh.bin"
    else:
        ext = "bin"
    with open(f"entry_{i}.{ext}", "wb") as f:
        f.write(content)
```

Further, the mesh data entries can be parsed into their individual sections with `parse_mesh_chunks`
(but a parser for these sections is not yet available).
