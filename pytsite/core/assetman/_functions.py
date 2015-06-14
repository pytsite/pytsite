"""Asset Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path
from importlib.util import find_spec
from pytsite.core import router

__packages = {}
__global_links = {'css': [], 'js': []}
__pattern_links = {}
__links = {}

def register_package(package_name: str, assets_dir: str='assets'):
    """Register assets container.
    """
    spec = find_spec(package_name)
    if not spec:
        raise Exception("Package '{}' is not found.".format(package_name))

    dir_path = path.join(path.dirname(spec.origin), assets_dir)
    if not path.isdir(dir_path):
        FileNotFoundError("Directory '{}' is not found.".format(dir_path))

    __packages[package_name] = dir_path


def get_packages() -> dict:
    return __packages


def add_location(location: str, collection: str, route_path: str=None):
    """Add an asset location to the collection.
    """
    if not route_path:
        route_path = router.current_path(True)

    if route_path == '*':
        __global_links[collection].append(location)
    elif route_path.endswith('*'):
        if route_path.endswith('/*'):
            route_path = route_path.replace('/*', '*')
        if route_path not in __pattern_links:
            __pattern_links[route_path] = {'css': [], 'js': []}
        if location not in __pattern_links[route_path][collection]:
            __pattern_links[route_path][collection].append(location)
    else:
        if route_path not in __links:
            __links[route_path] = {'css': [], 'js': []}
        if location not in __links[route_path][collection]:
            __links[route_path][collection].append(location)


def add_js(location: str, route_path: str=None):
    """Add a JS asset location to the collection.
    """
    add_location(location, 'js', route_path)


def add_css(location: str, route_path: str=None):
    """Add a CSS asset location to the collection.
    """
    add_location(location, 'css', route_path)


def add(location: str, route_path: str=None):
    """Shortcut.
    """
    if location.endswith('.js'):
        add_js(location, route_path)
    elif location.endswith('.css'):
        add_css(location, route_path)
    else:
        raise ValueError("Cannot detect collection to add for '{}'.".format(location))


def get_locations(collection: str) -> list:
    r = []
    current_path = router.current_path(True)

    # Links for every path
    for location in __global_links[collection]:
        r.append(location)

    # Links for pattern paths
    for glob_key in __pattern_links:
        if current_path.startswith(glob_key.rstrip('*')):
            for location in __pattern_links[glob_key][collection]:
                if location not in r:
                    r.append(location)

    # Links for exact path
    if current_path in __links:
        for location in __links[current_path][collection]:
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
    return router.url('/assets/{}/{}'.format(package_name, asset_path), strip_lang=True)


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
