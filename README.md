In which I attempt to reverse engineer Apple Look Around.

## Coverage tiles
Coverage can be found via XYZ tiles with z=17. The response is a binary protobuf object. I've identified the pano ID and the timestamp, but I have no idea what the other values are.
Most importantly, I don't know how to get the lat/lon of a panorama, so the best we've got for now is knowing that it's somewhere within the bounding box of the requested tile.

```python
from lookaround import get_coverage_tile_by_latlon
tile = get_coverage_tile_by_latlon(49.49277003930681, 6.588420315065048)
print(len(tile.pano))  # amount of panos on this tile
print(tile.pano[0])  # metadata of the first pano in the list: 
                     # its ID, the date and time it was taken, 
                     # and a lot of values I haven't deciphered yet
print(tile.unknown13.last_part_of_pano_url) # some sort of regional ID, we'll need this later
```

## Authentication
Requests for the actual image data must be authenticated.
The code for this is a translation of [retroplasma/flyover-reverse-engineering](https://github.com/retroplasma/flyover-reverse-engineering) (without which
none of this would be possible).

```python
from lookaround.auth import Authenticator
auth = Authenticator()
url = auth.authenticate_url("https://gspe72-ssl.ls.apple.com/mnn_us/0665/1337/7609/6445/9400/1095101453/t/0/2")
```

## Downloading imagery
Now that we can find panoramas near a location (roughly) and authenticate our download requests, let's go download one.
I don't know how to stitch these together yet (or if you'd even need to) because it's not quite as straightforward as it is with Street View, but
we can at the very least look at the raw images.

```python
from lookaround import fetch_pano_segment
from lookaround.auth import Authenticator
auth = Authenticator()
panoid = 11557400394790844462
that_other_id = 1203880071 # that weird other ID mentioned above
                           # which you get from the map tile
zoom = 2 # resolution / zoom level. 0 is highest, 7 is lowest.
for segment in range(0, 6): # segment to download. 0-3 are the sides, 4 is up, 5 is down.
    image = fetch_pano_segment(panoid, that_other_id, segment, zoom, auth)
    with open(f"{panoid}_{segment}_{zoom}.heic", "wb") as f:
        f.write(image)
```

Images are returned as HEIC, so you may need to install some plugins to view them.
