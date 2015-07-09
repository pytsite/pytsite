"""Asset Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path as _path
from importlib.util import find_spec as _find_spec
from pytsite.core import router as _router

__packages = {}
__global_links = {'css': [], 'js': []}
__pattern_links = {}
__exact_links = {}


def register_package(package_name: str, assets_dir: str='assets'):
    """Register assets container.
    """
    spec = _find_spec(package_name)
    if not spec:
        raise Exception("Package '{}' is not found.".format(package_name))

    dir_path = _path.join(_path.dirname(spec.origin), assets_dir)
    if not _path.isdir(dir_path):
        FileNotFoundError("Directory '{}' is not found.".format(dir_path))

    __packages[package_name] = dir_path


def get_packages() -> dict:
    return __packages


def add_location(location: str, collection: str, route_path: str=None):
    """Add an asset location.
    """
    if not location.startswith('http'):
        if not location.startswith('app') and not location.startswith('pytsite.'):
            location = 'pytsite.' + location

    if not route_path:
        route_path = _router.current_path(True)

    # Any path
    if route_path == '*':
        __global_links[collection].append(location)

    # Prefixed paths group
    elif route_path.endswith('*'):
        if route_path.endswith('/*'):
            route_path = route_path.replace('/*', '*')
        if route_path not in __pattern_links:
            __pattern_links[route_path] = {'css': [], 'js': []}
        if location not in __pattern_links[route_path][collection]:
            __pattern_links[route_path][collection].append(location)

    # Exact path
    else:
        if route_path not in __exact_links:
            __exact_links[route_path] = {'css': [], 'js': []}
        if location not in __exact_links[route_path][collection]:
            __exact_links[route_path][collection].append(location)


def remove_location(location: str, collection: str, route_path: str=None):
    """Remove an asset location.
    """
    if not location.startswith('http'):
        if not location.startswith('app') and not location.startswith('pytsite.'):
            location = 'pytsite.' + location

    if not route_path:
        route_path = _router.current_path(True)

    # Any path
    if route_path == '*':
        __global_links[collection] = [em for em in __global_links[collection] if em != location]

    # Prefixed paths group
    elif route_path.endswith('*'):
        if route_path.endswith('/*'):
            route_path = route_path.replace('/*', '*')
        if route_path not in __pattern_links:
            return
        __pattern_links[route_path][collection] = [em for em in __pattern_links[route_path][collection]
                                                   if em != location]

    # Exact path
    else:
        if route_path not in __exact_links:
            return
        __exact_links[route_path][collection] = [em for em in __exact_links[route_path][collection] if em != location]


def add(location: str, route_path: str=None):
    """Shortcut.
    """
    if location.endswith('.js'):
        add_location(location, 'js', route_path)
    elif location.endswith('.css'):
        add_location(location, 'css', route_path)
    else:
        raise ValueError("Cannot detect collection to add for '{}'.".format(location))


def remove(location: str, route_path: str=None):
    if location.endswith('.js'):
        remove_location(location, 'js', route_path)
    elif location.endswith('.css'):
        remove_location(location, 'css', route_path)
    else:
        raise ValueError("Cannot detect collection to add for '{}'.".format(location))


def get_locations(collection: str) -> list:
    r = []
    current_path = _router.current_path(True)

    # Links for every path
    for location in __global_links[collection]:
        r.append(location)

    # Links for pattern paths
    for glob_key in __pattern_links:
        if current_path.startswith(glob_key.rstrip('*')):
            for location in __pattern_links[glob_key][collection]:
                if location not in r:
                    r.append(location)

    # Links for exact paths
    if current_path in __exact_links:
        for location in __exact_links[current_path][collection]:
            if location not in r:
                r.append(location)

    return r


def dump_js() -> str:
    """Dump JS links.
    """
    r = ''
    for location in get_locations('js'):
        r += '<script type="text/javascript" src="{}"></script>\n'.format(get_url(location))

    return r


def dump_css() -> str:
    """Dump CSS links.
    """
    r = ''
    for location in get_locations('css'):
        r += '<link rel="stylesheet" href="{}">\n'.format(get_url(location))

    return r


def get_url(location: str) -> str:
    """Get URL of an asset.
    """
    if location.startswith('http'):
        return location
    package_name, asset_path = __split_asset_location_info(location)
    return _router.url('/assets/{}/{}'.format(package_name, asset_path), strip_lang=True)


def __split_asset_location_info(location: str) -> dict:
    """Split asset path into package name and asset path.
    """
    package_name = 'app'
    asset_path = location
    path_parts = location.split('@')
    if len(path_parts) == 2:
        package_name = path_parts[0]
        asset_path = path_parts[1]

    if package_name not in __packages:
        raise Exception("Package '{}' is not registered.".format(package_name))

    return package_name, asset_path
