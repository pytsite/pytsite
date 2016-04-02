"""Asset Manager.
"""
from os import path as _path
from importlib.util import find_spec as _find_spec
from pytsite import router as _router, threading as _threading, util as _util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_packages = {}

_locations = {}
_last_weight = {}

_p_locations = {}
_last_p_weight = 0

_inline = {}
_last_i_weight = {}


def register_package(package_name: str, assets_dir: str = 'res/assets'):
    """Register assets container.
    """
    spec = _find_spec(package_name)
    if not spec:
        raise RuntimeError("Package '{}' is not found.".format(package_name))

    dir_path = _path.join(_path.dirname(spec.origin), assets_dir)
    if not _path.isdir(dir_path):
        FileNotFoundError("Directory '{}' is not found.".format(dir_path))

    if package_name in _packages:
        raise RuntimeError("Package '{}' is already registered.".format(package_name))

    _packages[package_name] = dir_path


def get_packages() -> dict:
    """Get registered packages.
    """
    return _packages


def detect_collection(location: str) -> str:
    if location.find('.js') > 0:
        return 'js'
    elif location.find('.css') > 0:
        return 'css'
    else:
        raise ValueError("Cannot determine collection of location '{}'.".format(location))


def add(location: str, permanent: bool = False, collection: str = None, weight: int = 0, path_prefix: str = None):
    """Add an asset.
    """
    # Determine collection
    if not collection:
        collection = detect_collection(location)

    if path_prefix and not path_prefix.startswith('/'):
        path_prefix = '/' + path_prefix

    tid = _threading.get_id()
    if tid not in _locations:
        _locations[tid] = {}

    location_hash = hash((location, path_prefix))

    if location_hash not in _p_locations and location_hash not in _locations[tid]:
        if permanent:
            global _last_p_weight

            if not weight:
                _last_p_weight += 10
                weight = _last_p_weight
            elif weight > _last_p_weight:
                _last_p_weight = weight

            _p_locations[location_hash] = (location, collection, weight, path_prefix)
        else:
            if not weight:
                _last_weight[tid] += 10
                weight = _last_weight[tid]
            elif weight > _last_weight[tid]:
                _last_weight[tid] = weight

            _locations[tid][location_hash] = (location, collection, weight, path_prefix)


def add_inline(s: str, weight=0):
    """Add a code which intended to output in the document.
    """
    tid = _threading.get_id()

    if not weight:
        _last_i_weight[tid] += 10
    elif weight > _last_i_weight[tid]:
        _last_i_weight[tid] = weight

    _inline[tid].append((s, weight))


def remove(location):
    """Remove an asset location.
    """
    tid = _threading.get_id()
    if tid not in _locations:
        return

    # Location as a string
    if isinstance(location, str):
        _locations[tid] = {k: v for k, v in _locations[tid].items() if location != v[0]}
    # Location as a compiled regular expression
    elif not isinstance(location, str) and location.__class__.__name__ == 'SRE_Pattern':
        _locations[tid] = {k: v for k, v in _locations[tid].items() if not location.match(v[0])}
    else:
        raise TypeError('String or compiled regular expression expected.')


def reset():
    """Remove all previously added locations and inline code except 'permanent'.
    """
    global _last_weight

    tid = _threading.get_id()

    _locations[tid] = {}
    _last_weight[tid] = 0
    _inline[tid] = []
    _last_i_weight[tid] = 0


def get_locations(collection: str = None, filter_path: bool = True) -> tuple:
    tid = _threading.get_id()

    p_locations = _p_locations.values()
    locations = _locations[tid].values()

    locations = sorted(p_locations, key=lambda x: x[2]) + sorted(locations, key=lambda x: x[2])

    # Filter by collection
    if collection:
        locations = [l for l in locations if l[1] == collection]

    # Filter by path
    if filter_path:
        current_path = _router.current_path()
        locations = [l for l in locations if (l[3] is None or current_path.startswith(l[3]))]

    # Build unique list.
    # Duplicates are possible because same location may be added more than once with different path prefixes.
    added = []
    r = []
    for l in locations:
        if l[0] not in added:
            added.append(l[0])
            r.append(l)

    return r


def get_inline() -> list:
    tid = _threading.get_id()
    if tid not in _inline:
        return []

    return sorted(_inline[tid], key=lambda x: x[1])


def dump_js(html_escape: bool = True) -> str:
    """Dump JS links.
    """
    r = ''
    for loc_url in get_urls('js'):
        if html_escape:
            loc_url = _util.escape_html(loc_url)
        r += '<script type="text/javascript" src="{}"></script>\n'.format(loc_url)

    return r


def dump_css(html_escape: bool = True) -> str:
    """Dump CSS links.
    """
    r = ''
    for loc_url in get_urls('css'):
        if html_escape:
            loc_url = _util.escape_html(loc_url)
        r += '<link rel="stylesheet" href="{}">\n'.format(loc_url)

    return r


def dump_inline() -> str:
    r = ''

    tid = _threading.get_id()
    if tid in _inline:
        for item in _inline[tid]:
            r += item[0]

    return r


def url(location: str) -> str:
    """Get URL of an asset.
    """
    if location.startswith('http') or location.startswith('//'):
        return location

    package_name, asset_path = _split_asset_location_info(location)

    return _router.url('/assets/{}/{}'.format(package_name, asset_path), strip_lang=True)


def get_urls(collection: str = None, filter_path: bool = True) -> list:
    """Get URLs of all locations in the collection.
    """
    return [url(l[0]) for l in get_locations(collection, filter_path)]


def _split_asset_location_info(location: str) -> dict:
    """Split asset path into package name and asset path.
    """
    package_name = 'app'
    asset_path = location
    path_parts = location.split('@')
    if len(path_parts) == 2:
        package_name = path_parts[0]
        asset_path = path_parts[1]

    if package_name not in _packages:
        raise RuntimeError("Package '{}' is not registered.".format(package_name))

    return package_name, asset_path
