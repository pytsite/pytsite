"""PytSite Asset Manager.
"""
import re as _re
import subprocess as _subprocess
from os import path as _path, walk as _walk, makedirs as _makedirs
from shutil import rmtree as _rmtree, copy as _copy
from webassets import Environment as _Environment, Bundle as _Bundle
from webassets.script import CommandLineEnvironment as _CommandLineEnvironment
from webassets.filter.less import Less as LessFilter
from importlib.util import find_spec as _find_spec
from pytsite import router as _router, threading as _threading, util as _util, reg as _reg, logger as _logger, \
    events as _events, maintenance as _maintenance, console as _console, lang as _lang, theme as _theme
from . import _error

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

_globals = {}


def register_package(package_name: str, assets_dir: str = 'res/assets', alias: str = None):
    """Register assets container.
    """
    pkg_spec = _find_spec(package_name)
    if not pkg_spec:
        raise RuntimeError("Package '{}' is not found.".format(package_name))

    dir_path = _path.abspath(_path.join(_path.dirname(pkg_spec.origin), assets_dir))
    if not _path.isdir(dir_path):
        FileNotFoundError("Directory '{}' is not found.".format(dir_path))

    if alias:
        package_name = alias

    if package_name in _packages:
        raise _error.PackageAlreadyRegistered("Package '{}' is already registered.".format(package_name))

    _packages[package_name] = dir_path


def is_package_registered(package_name_or_alias: str):
    """Check if the package is registered.
    """
    return package_name_or_alias in _packages


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


def add(location: str, permanent: bool = False, collection: str = None, weight: int = 0, path_prefix: str = None,
        async: bool = False, defer: bool = False):
    """Add an asset.
    """
    if not permanent and not _router.request():
        raise RuntimeError('Non permanent assets only allowed while processing HTTP requests.')

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

            _p_locations[location_hash] = (location, collection, weight, path_prefix, async, defer)
        else:
            if not weight:
                _last_weight[tid] += 10
                weight = _last_weight[tid]
            elif weight > _last_weight[tid]:
                _last_weight[tid] = weight

            _locations[tid][location_hash] = (location, collection, weight, path_prefix, async, defer)


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
    for loc in get_locations('js'):
        l_url = url(_util.escape_html(loc[0])) if html_escape else url(loc[0])
        l_async = ' async' if loc[4] else ''
        l_defer = ' defer' if loc[5] else ''

        r += '<script type="text/javascript" src="{}"{}{}></script>\n'.format(l_url, l_async, l_defer)

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


def register_global(name: str, value, overwrite: bool = False):
    """Define a global variable which can be user by LESS compiler, etc.
    """
    global _globals

    if name in _globals and not overwrite:
        raise KeyError("Global '{}' is already defined with value {}".format(name, value))

    _globals[name] = value


def build(package_name: str = None, maintenance: bool = True, cache: bool = True):
    """Compile assets.
    """
    global _globals

    # Check for LESS compiler existence
    if _subprocess.run(['which', 'lessc'], stdout=_subprocess.PIPE).returncode:
        raise RuntimeError('lessc executable is not found. Check http://lesscss.org/#using-less-installation.')

    _events.fire('pytsite.assetman.build.before')

    # Paths
    assets_dir = _path.join(_reg.get('paths.static'), 'assets')

    # Determine list of packages to process
    packages_list = get_packages()
    if package_name:
        try:
            packages_list = {package_name: packages_list[package_name]}
        except KeyError:
            raise _error.PackageNotRegistered("Assetman package '{}' is not registered.".format(package_name))

    # Enable maintenance mode
    if maintenance:
        _maintenance.enable()

    # Delete target assets directory if we going to compile all packages
    if not package_name and _path.exists(assets_dir):
        _rmtree(assets_dir)

    _console.print_info(_lang.t('pytsite.assetman@compiling_assets'))
    for pkg_name, source_dir_path in packages_list.items():
        # Initialize cache storage
        cache_dir = None
        if cache:
            cache_dir = _path.join(_reg.get('paths.tmp'), 'assetman', pkg_name)
            if not _path.isdir(cache_dir):
                _makedirs(cache_dir, 0o755)

        # Building package's assets absolute paths list
        src_file_paths = []
        for root, dirs, files in _walk(source_dir_path):
            for file in files:
                src_file_paths.append(_path.join(root, file))

        # Create Webassets environment
        env = _Environment(directory=source_dir_path, versions=False, manifest=False, cache=cache_dir)

        # Process each package's asset
        for src_path in src_file_paths:
            dst_path = _path.join(assets_dir, pkg_name, src_path.replace(source_dir_path + _path.sep, ''))

            ext = _path.splitext(src_path)[1]
            if ext in ['.js', '.css', '.ts', '.less']:
                filters = []

                # LESS compiler
                if ext == '.less':
                    args = ['--modify-var={}={}'.format(k, v) for k, v in _globals.items()]
                    filters.append(LessFilter(extra_args=args))
                    dst_path = _re.sub(r'\.less$', '.css', dst_path)
                    ext = '.css'

                # TypeScript compiler
                elif ext == '.ts':
                    filters.append('typescript')
                    dst_path = _re.sub(r'\.ts$', '.js', dst_path)
                    ext = '.js'

                # Minifying JS/CSS
                if _reg.get('output.minify'):
                    if ext == '.js' and not src_path.endswith('.min.js') and not src_path.endswith('.pack.js'):
                        filters.append('jsmin')
                    if ext == '.css' and not src_path.endswith('.min.css'):
                        filters.append('cssmin')

                # Add asset to environment as separate bundle
                bundle = _Bundle(src_path, filters=filters)
                env.register(dst_path, bundle, output=dst_path)

            # Just copy file as is
            else:
                dst_dir = _path.dirname(dst_path)
                if not _path.exists(dst_dir):
                    _makedirs(dst_dir, 0o755)
                _copy(src_path, dst_path)

        # Build environment
        cmd = _CommandLineEnvironment(env, _logger)
        if cmd.invoke('build', {}) == 2:
            raise RuntimeError("Error while compiling assets for package '{}'. Check logs for details.".
                               format(pkg_name))

    _events.fire('pytsite.assetman.build')

    if maintenance:
        _maintenance.disable()


def _split_asset_location_info(location: str) -> dict:
    """Split asset path into package name and asset path.
    """
    if '@' not in location:
        location = '$theme@' + location

    if '$theme' in location:
        location = location.replace('$theme', _theme.get_current())

    pkg_name, asset_path = location.split('@')[:2]

    if pkg_name not in _packages:
        raise _error.PackageNotRegistered("Assetman package '{}' is not registered.".format(pkg_name))

    return pkg_name, asset_path
