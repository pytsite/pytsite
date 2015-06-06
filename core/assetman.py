"""Asset Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path, makedirs, walk
from shutil import rmtree, copy
from webassets import Environment
from webassets.script import CommandLineEnvironment
from importlib.util import find_spec
from . import console, lang, router, logger, reg, events


class ConsoleCommand(console.AbstractCommand):
    def get_name(self) -> str:
        return 'assetman:build'

    def get_description(self) -> str:
        return lang.t('pytsite.core@assetman_console_command_description')

    def execute(self, **kwargs: dict):
        compile_assets()
        lang.compile_translations()


_packages = {}
_links = {'js': [], 'css': []}


def register_package(package_name: str, assets_dir: str='assets'):
    """Register assets container.
    """

    spec = find_spec(package_name)
    if not spec:
        raise Exception("Package '{}' is not found.".format(package_name))

    dir_path = path.join(path.dirname(spec.origin), assets_dir)
    if not path.isdir(dir_path):
        FileNotFoundError("Directory '{}' is not found.".format(dir_path))

    _packages[package_name] = dir_path


def add_location(location: str, collection: str):
    """Add an asset location to the collection.
    """

    if collection not in _links:
        _links[collection] = []

    if location not in _links[collection]:
        _links[collection].append(location)


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
    for k in _links:
        _links[k] = []

    add_js('pytsite.core@js/jquery-2.1.4.min.js')
    add_js('pytsite.core@js/assetman.js')
    add_js('pytsite.core@js/lang.js')

    if reg.get('core.jquery_ui.enabled'):
        add_css('pytsite.core@jquery-ui/jquery-ui.min.css')
        add_js('pytsite.core@jquery-ui/jquery-ui.min.js')
        add_js('pytsite.core@jquery-ui/i18n/datepicker-{}.js'.format(lang.get_current_lang()))

    events.fire('pytsite.core.assetman.request')


def dump_js() -> str:
    """Dump JS links.
    """

    r = ''
    for location in _links['js']:
        r += '<script type="text/javascript" src="{0}"></script>\n'.format(get_url(location))
    return r


def dump_css() -> str:
    """Dump CSS links.
    """

    r = ''
    for location in _links['css']:
        r += '<link rel="stylesheet" href="{0}">\n'.format(get_url(location))
    return r


def get_url(location: str) -> str:
    """Get URL of an asset.
    """

    package_name, asset_path = __split_asset_location_info(location)
    return router.url('/assets/{0}/{1}'.format(package_name, asset_path), strip_lang=True)


def compile_assets():
    """Compile assets.
    """

    static_dir = reg.get('paths.static')
    debug = reg.get('debug.enabled')

    if path.exists(static_dir):
        rmtree(static_dir)

    for pkg_name, package_assets_dir in _packages.items():
        # Building package's assets absolute paths list
        files_list = []
        for root, dirs, files in walk(package_assets_dir):
            for file in files:
                files_list.append(path.join(root, file))

        for src in files_list:
            if '.webassets-cache' in src:
                continue

            dst = src.replace(package_assets_dir + path.sep, '')
            dst = path.join(static_dir, 'assets', pkg_name, dst)
            print('Compiling {} -> {}'.format(src, dst))

            ext = path.splitext(src)[1]
            if ext in ['.js', '.css']:
                filters = None

                if ext == '.js' and not src.endswith('.min.js'):
                    filters = 'rjsmin'

                if ext == '.css' and not src.endswith('.min.css'):
                    filters = 'cssutil'

                env = Environment(directory=package_assets_dir, filters=filters, debug=debug)
                env.register('bundle', src, output=dst)
                cmd = CommandLineEnvironment(env, logger)
                cmd.invoke('build', dict())
            elif '.webassets-cache' not in src:
                dst_dir = path.dirname(dst)
                if not path.exists(dst_dir):
                    makedirs(dst_dir, 0o755)
                copy(src, dst)


def __split_asset_location_info(location: str) -> dict:
    """Split asset path into package name and asset path.
    """
    package_name = 'app'
    asset_path = location
    path_parts = location.split('@')
    if len(path_parts) == 2:
        package_name = path_parts[0]
        asset_path = path_parts[1]

    if package_name not in _packages:
        raise Exception("Package '{0}' is not registered.".format(package_name))

    return package_name, asset_path
