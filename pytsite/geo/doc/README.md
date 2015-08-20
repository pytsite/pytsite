# Pytsite Geo Plugin

## Functions

### pytsite.geo.get_map_link()
Signature: `get_map_link(query: str='', lng: float=None, lat: float=None) -> str`

## ODM Fields

### pytsite.geo.field.Location
Stores geo location information.

#### Format of the value
Dictionary with keys: `address`, `lng_lat`, `components`. All keys are required.

- `lng: float` -- longitude.
- `lat: float` -- latitude.
- `alt: float` -- altitude.
- `accuracy: float` -- position accuracy.
- `alt_accuracy: float` -- altitude accuracy.
- `heading: float` -- heading.
- `speed: float` -- speed.
- `address: str` -- address string.
- `address_components: list` -- [address components](https://developers.google.com/maps/documentation/geocoding/intro#Types).


## Widgets

### pytsite.geo.widget.SearchAddress
Address search text input with autocomplete.

#### Arguments
- `autodetect: bool=False` -- whether to fill the widget automatically.

#### Format of the value
See `pytsite.geo.field.Location`.  


### pytsite.geo.widget.StaticMap
Image of the map with marker.

#### Arguments
- `language: str` -- language of the map. Default is current language.
- `zoom: int=13` -- zoom of the map.
- `lat: float=51.48` -- latitude.
- `lng: float=0.0` -- longitude.
- `width: int=320` -- width of the image.
- `height: int=240` -- height of the image.
- `address: str=''` -- address string.
- `link: bool=True` -- whether to link map's image to the Google Maps URL.


## Validation Rules

### pytsite.geo.rule.AddressNotEmpty
Checks if the address structure is filled completely.

#### Format of the value
See `pytsite.geo.field.Location`.
