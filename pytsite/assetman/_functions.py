"""Asset Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path as _path
from importlib.util import find_spec as _find_spec

from pytsite import router as _router

_packages = {}
_links = {'css': [], 'js': []}


def register_package(package_name: str, assets_dir: str='res/assets'):
    """Register assets container.
    """
    spec = _find_spec(package_name)
    if not spec:
        raise Exception("Package '{}' is not found.".format(package_name))

    dir_path = _path.join(_path.dirname(spec.origin), assets_dir)
    if not _path.isdir(dir_path):
        FileNotFoundError("Directory '{}' is not found.".format(dir_path))

    _packages[package_name] = dir_path


def get_packages() -> dict:
    """Get registered packages.
    """
    return _packages


def add(location: str, collection: str=None):
    """Shortcut.
    """
    if not collection:
        if location.endswith('.js'):
            collection = 'js'
        elif location.endswith('.css'):
            collection = 'css'
        else:
            raise ValueError("Cannot detect collection of '{}'.".format(location))

    if location not in _links[collection]:
        _links[collection].append(location)


def remove(location: str, collection: str=None):
    """Remove an asset location.
    """
    if not collection:
        if location.endswith('.js'):
            collection = 'js'
        elif location.endswith('.css'):
            collection = 'css'
        else:
            raise ValueError("Cannot detect collection of '{}'.".format(location))

    _links[collection] = [em for em in _links[collection] if em != location]


def reset():
    """Remove all previously added locations.
    """
    global _links
    _links = {'css': [], 'js': []}


def get_locations(collection: str) -> list:
    return [l for l in _links[collection]]


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
    if location.startswith('http') or location.startswith('//'):
        return location
    package_name, asset_path = _split_asset_location_info(location)

    return _router.url('/assets/{}/{}'.format(package_name, asset_path), strip_lang=True)


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
        raise Exception("Package '{}' is not registered.".format(package_name))

    return package_name, asset_path