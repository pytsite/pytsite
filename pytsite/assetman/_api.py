"""Asset Manager.
"""
from os import path as _path
from importlib.util import find_spec as _find_spec
from pytsite import router as _router, threading as _threading

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_packages = {}
_locations = {}
_last_weight = {}
_last_permanent_weight = {}
_last_inline_weight = {}
_inline = {}


def register_package(package_name: str, assets_dir: str='res/assets'):
    """Register assets container.
    """
    spec = _find_spec(package_name)
    if not spec:
        raise RuntimeError("Package '{}' is not found.".format(package_name))

    dir_path = _path.join(_path.dirname(spec.origin), assets_dir)
    if not _path.isdir(dir_path):
        FileNotFoundError("Directory '{}' is not found.".format(dir_path))

    tid = _threading.get_id()
    if tid not in _packages:
        _packages[tid] = {}

    if package_name in _packages[tid]:
        raise RuntimeError("Package '{}' is already registered.".format(package_name))

    _packages[tid][package_name] = dir_path


def get_packages() -> dict:
    """Get registered packages.
    """
    tid = _threading.get_id()
    if tid not in _packages:
        _packages[tid] = {}

    return _packages[tid]


def add(location: str, collection: str=None, weight=0, permanent=False):
    """Add an asset.
    """
    # Determine collection
    if not collection:
        if location.endswith('.js'):
            collection = 'js'
        elif location.endswith('.css'):
            collection = 'css'
        else:
            raise ValueError("Cannot determine collection of location '{}'.".format(location))

    tid = _threading.get_id()
    if tid not in _locations:
        _locations[tid] = {}
        _last_weight[tid] = 0

    # Add only if it isn't added yet
    if location not in _locations[tid]:
        # Determine weight
        if not weight:
            _last_weight[tid] += 10
            weight = _last_weight[tid]

        elif weight > _last_weight[tid]:
            _last_weight[tid] = weight

        if permanent:
            _last_permanent_weight[tid] = weight

        _locations[tid][location] = (collection, weight, permanent)


def add_inline(s: str, weight=0, forever=False):
    """Add a code which intended to output in the document.
    """
    tid = _threading.get_id()
    if tid not in _inline:
        _inline[tid] = []

    if not weight:
        _last_inline_weight[tid] += 10
    elif weight > _last_inline_weight[tid]:
        _last_inline_weight[tid] = weight

    _inline[tid].append((s, weight, forever))


def remove(location):
    """Remove an asset location.
    """
    tid = _threading.get_id()
    if tid not in _locations:
        return

    if isinstance(location, str):
        _locations[tid] = {k: v for k, v in _locations[tid] if k != location}

    # Compiled regular expression
    elif not isinstance(location, str) and location.__class__.__name__ == 'SRE_Pattern':
        _locations[tid] = {k: v for k, v in _locations[tid] if not location.match(k)}

    else:
        raise TypeError('String or compiled regular expression expected.')


def reset():
    """Remove all previously added locations and inline code except 'permanent'.
    """
    tid = _threading.get_id()

    # Filter out all except 'permanent' items
    if tid in _locations:
        _locations[tid] = {k: v for k, v in _locations[tid].items() if v[2]}

    # Filter out all inline code except 'permanent' items
    if tid in _inline:
        _inline[tid] = [s for s in _inline[tid] if s[2]]

    if tid not in _last_permanent_weight:
        _last_permanent_weight[tid] = 0

    if tid not in _last_weight:
        _last_weight[tid] = 0

    # Non-permanent locations should never stand before permanent ones
    _last_weight[tid] = _last_permanent_weight[tid]


def get_locations(collection: str=None) -> list:
    tid = _threading.get_id()

    if tid not in _locations:
        return []

    if collection:
        # Select all locations of particular collection
        locations = [(k, v[0], v[1], v[2]) for k, v in _locations[tid].items() if v[0] == collection]
    else:
        # All locations
        locations = [(k, v[0], v[1], v[2]) for k, v in _locations[tid].items()]

    # Sort by weight
    return [l for l in sorted(locations, key=lambda x: x[2])]


def get_inline() -> list:
    tid = _threading.get_id()
    if tid not in _inline:
        return []

    return sorted(_inline[tid], key=lambda x: x[1])


def dump_js() -> str:
    """Dump JS links.
    """
    r = ''
    for loc_url in get_urls('js'):
        r += '<script type="text/javascript" src="{}"></script>\n'.format(loc_url)

    return r


def dump_css() -> str:
    """Dump CSS links.
    """
    r = ''
    for loc_url in get_urls('css'):
        r += '<link rel="stylesheet" href="{}">\n'.format(loc_url)

    return r


def dump_inline() -> str:
    r = ''

    tid = _threading.get_id()
    if tid in _inline:
        for item in _inline:
            r += item[0]

    return r


def url(location: str) -> str:
    """Get URL of an asset.
    """
    if location.startswith('http') or location.startswith('//'):
        return location

    package_name, asset_path = _split_asset_location_info(location)

    return _router.url('/assets/{}/{}'.format(package_name, asset_path), strip_lang=True)


def get_urls(collection: str=None) -> list:
    """Get URLs of all locations in the collection.
    """
    return [url(l[0]) for l in get_locations(collection)]


def _split_asset_location_info(location: str) -> dict:
    """Split asset path into package name and asset path.
    """
    tid = _threading.get_id()
    if tid not in _packages:
        _packages[tid] = {}

    package_name = 'app'
    asset_path = location
    path_parts = location.split('@')
    if len(path_parts) == 2:
        package_name = path_parts[0]
        asset_path = path_parts[1]

    if package_name not in _packages[tid]:
        raise RuntimeError("Package '{}' is not registered.".format(package_name))

    return package_name, asset_path
