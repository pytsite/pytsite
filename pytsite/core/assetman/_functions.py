"""Asset Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path
from importlib.util import find_spec
from pytsite.core import lang, router, reg, events

__packages = {}
__links = {'js': [], 'css': []}


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


def add_location(location: str, collection: str):
    """Add an asset location to the collection.
    """

    if collection not in __links:
        __links[collection] = []

    if location not in __links[collection]:
        __links[collection].append(location)


def add_js(location: str):
    """Add a JS asset location to the collection.
    """
    add_location(location, 'js')


def add_css(location: str):
    """Add a CSS asset location to the collection.
    """
    add_location(location, 'css')


def add(location: str):
    """Shortcut.
    """
    if location.endswith('.js'):
        add_js(location)
    elif location.endswith('.css'):
        add_css(location)
    else:
        raise ValueError("Cannot detect collection to add for '{}'.".format(location))


def reset():
    """Clear added locations.
    """
    for k in __links:
        __links[k] = []

    add('pytsite.core@js/jquery-2.1.4.min.js')
    add('pytsite.core@js/assetman.js')
    add('pytsite.core@js/lang.js')

    if reg.get('core.jquery_ui.enabled'):
        add('pytsite.core@jquery-ui/jquery-ui.min.css')
        add('pytsite.core@jquery-ui/jquery-ui.min.js')
        add('pytsite.core@jquery-ui/i18n/datepicker-{}.js'.format(lang.get_current_lang()))


def dump_js() -> str:
    """Dump JS links.
    """
    r = ''
    for location in __links['js']:
        r += '<script type="text/javascript" src="{}"></script>\n'.format(get_url(location))
    return r


def dump_css() -> str:
    """Dump CSS links.
    """
    r = ''
    for location in __links['css']:
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
