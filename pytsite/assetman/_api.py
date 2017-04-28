"""PytSite Asset Manager
"""
import subprocess as _subprocess
import json as _json
from typing import Dict as _Dict, List as _List, Tuple as _Tuple, Union as _Union, Callable as _Callable, \
    Iterable as _Iterable
from os import path as _path, chdir as _chdir, makedirs as _makedirs
from shutil import rmtree as _rmtree
from importlib.util import find_spec as _find_spec
from pytsite import router as _router, threading as _threading, util as _util, reg as _reg, events as _events, \
    maintenance as _maintenance, console as _console, lang as _lang, theme as _theme, tpl as _tpl
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_package_paths = {}  # type: _Dict[str, str]
_package_aliases = {}  # type: _Dict[str, str]
_libraries = {}  # type: _Dict[str, _Union[_Iterable, _Callable[..., _Iterable]]]

_tasks = []  # type: _List[_Tuple]
_requirejs_modules = {}  # type: _Dict[str, str]

_locations = {}
_last_weight = {}

_p_locations = {}
_last_p_weight = 0

_inline = {}
_last_i_weight = {}

_globals = {}

_NODE_BIN_DIR = _path.join(_reg.get('paths.root'), 'node_modules', '.bin')
_REQUIRED_NPM_PACKAGES = [
    'gulp', 'gulp-rename', 'gulp-ignore', 'gulp-minify', 'gulp-less', 'gulp-cssmin', 'gulp-babel',
    'babel-preset-es2015', 'gulp-browserify', 'babelify', 'vue', 'vueify', 'babel-plugin-transform-runtime'
]
_GULPFILE = _path.join(_path.realpath(_path.dirname(__file__)), 'gulpfile.js')
_GULP_TASKS_FILE = _path.join(_reg.get('paths.tmp'), 'gulp-tasks.json')


def _run_process(cmd: list, debug: bool = False) -> _subprocess.CompletedProcess:
    """Run process.
    """
    stdout = stderr = _subprocess.PIPE

    if debug and _reg.get('env.type') == 'console':
        stdout = stderr = None

    return _subprocess.run(cmd, stdout=stdout, stderr=stderr)


def _run_node_bin(bin_name: str, *args, **kwargs) -> _subprocess.CompletedProcess:
    """Run Node's binary.
    """
    args_l = []
    for k, v in kwargs.items():
        if isinstance(v, bool):
            v = 'yes' if v else 'no'
        args_l.append('--{}={}'.format(k, v))

    cmd = ['node', _NODE_BIN_DIR + _path.sep + bin_name] + args_l + list(args)

    try:
        r = _run_process(cmd, kwargs.get('debug', False))
        r.check_returncode()
        return r
    except _subprocess.CalledProcessError:
        raise RuntimeError('None-zero exit status while running command {}'.format(cmd))


def register_package(package_name: str, assets_dir: str = 'res/assets', alias: str = None):
    """Register assets container.
    """
    try:
        resolve_package_name(package_name)
        raise _error.PackageAlreadyRegistered(package_name)
    except _error.PackageNotRegistered:
        pass

    pkg_spec = _find_spec(package_name)
    if not pkg_spec:
        raise RuntimeError("Package '{}' is not found".format(package_name))

    dir_path = _path.abspath(_path.join(_path.dirname(pkg_spec.origin), assets_dir))
    if not _path.isdir(dir_path):
        FileNotFoundError("Directory '{}' is not found".format(dir_path))

    _package_paths[package_name] = dir_path

    if alias:
        if alias in _package_aliases:
            raise _error.PackageAliasAlreadyUsed(alias)

        _package_aliases[alias] = package_name


def library(name: str, assets: _Union[_List, _Callable[..., _List]]):
    """Define a library of assets.
    """
    if name in _libraries:
        raise _error.LibraryAlreadyRegistered(name)

    if is_package_registered(name):
        raise _error.PackageAlreadyRegistered(name)

    _libraries[name] = assets


def is_package_registered(package_name_or_alias: str):
    """Check if the package is registered.
    """
    return package_name_or_alias in _package_paths or package_name_or_alias in _package_aliases


def _get_package_path(package_name_or_alias: str) -> str:
    return _package_paths[resolve_package_name(package_name_or_alias)]


def resolve_package_name(package_name_or_alias) -> str:
    package_name = package_name_or_alias

    if package_name_or_alias in _package_aliases:
        package_name = _package_aliases[package_name_or_alias]

    if package_name not in _package_paths:
        raise _error.PackageNotRegistered(package_name_or_alias)

    return package_name


def detect_collection(location: str) -> str:
    if location.find('.js') > 0:
        return 'js'
    elif location.find('.css') > 0:
        return 'css'
    else:
        raise ValueError("Cannot determine collection of location '{}'.".format(location))


def preload(location: str, permanent: bool = False, collection: str = None, weight: int = 0, path_prefix: str = None,
            async: bool = False, defer: bool = False, **kwargs):
    """Add an asset.
    """
    if not permanent and not _router.request():
        raise RuntimeError('Non permanent assets only allowed while processing HTTP requests.')

    if location in _libraries:
        if callable(_libraries[location]):
            assets = _libraries[location](**kwargs)
        elif isinstance(_libraries[location], _Iterable):
            assets = _libraries[location]
        else:
            raise TypeError('Iterable expected')

        for asset_location in assets:
            preload(asset_location, permanent, collection, weight, path_prefix, async, defer)

        return

    # Determine collection
    if not collection:
        collection = detect_collection(location)

    if path_prefix and not path_prefix.startswith('/'):
        path_prefix = '/' + path_prefix

    tid = _threading.get_id()
    if tid not in _locations:
        _locations[tid] = {}

    location_hash = _util.md5_hex_digest(str((location, path_prefix)))

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


def get_locations(collection: str = None, filter_path: bool = True) -> list:
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

    package_name, asset_path = _split_location_info(location)

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


def setup():
    """Setup assetman environment.
    """
    # Node modules should be installed exactly to the root of the project to get things work
    _chdir(_reg.get('paths.root'))

    # Check for NPM existence
    if _run_process(['which', 'npm']).returncode != 0:
        raise RuntimeError('NPM executable is not found. Check https://docs.npmjs.com/getting-started/installing-node')

    # Install required public NPM packages
    if _run_process(['npm', 'install'] + _REQUIRED_NPM_PACKAGES).returncode != 0:
        raise RuntimeError('Error while installing NPM packages: {}'.format(_REQUIRED_NPM_PACKAGES))


def _add_task(location: str, task_name: str, dst: str = '', **kwargs):
    """Add a transformation task.
    """
    pkg_name, src = _split_location_info(location)
    src = _get_package_path(pkg_name) + _path.sep + src
    dst = _path.join(_reg.get('paths.assets'), pkg_name, dst)

    _tasks.append((pkg_name, task_name, src, dst, kwargs))


def t_copy(location: str, target: str = ''):
    """Add a location to the copy task.
    """
    _add_task(location, 'copy', target)


def t_copy_static(location: str, target: str = ''):
    """Add a location to the copy_static task.
    """
    _add_task(location, 'copy_static', target)


def t_css(location: str, target: str = ''):
    """Add a location to the CSS transform task.
    """
    _add_task(location, 'css', target)


def t_less(location: str, target: str = ''):
    """Add a location to the LESS transform task.
    """
    _add_task(location, 'less', target)


def t_js(location: str, target: str = '', babelify: bool = False):
    """Add a location to the JS transform task.
    """
    _add_task(location, 'js', target, babelify=babelify)


def t_browserify(location: str, target: str = '', babelify: bool = False, vueify: bool = False):
    """Add a location to the browserify transform task.
    """
    _add_task(location, 'browserify', target, babelify=babelify, vueify=vueify)


def js_module(name: str, location: str):
    """Define a RequireJS module.
    """
    if name in _requirejs_modules:
        raise ValueError("RequireJS module '{}' is already defined")

    _requirejs_modules[name] = location


def build(package_name: str = None, maintenance: bool = True):
    """Compile assets.
    """
    global _globals
    assets_static_path = _reg.get('paths.assets')

    # Enable maintenance mode
    if maintenance:
        _maintenance.enable()

    if package_name:
        package_name = resolve_package_name(package_name)

        package_assets_static_path = _path.join(assets_static_path, package_name)

        if _path.exists(package_assets_static_path):
            _rmtree(package_assets_static_path)
    elif _path.exists(assets_static_path):
        _rmtree(assets_static_path)

    _console.print_info(_lang.t('pytsite.assetman@compiling_assets'))

    _events.fire('pytsite.assetman.build.before')

    # Build tasks file for Gulp
    tasks_file_content = []
    for t_info in _tasks:
        pkg_name, task_name, src, dst, kwargs = t_info
        if not package_name or package_name == pkg_name:
            tasks_file_content.append({
                'name': task_name,
                'source': src,
                'destination': dst,
                'args': kwargs,
            })
    with open(_GULP_TASKS_FILE, 'wt') as f:
        f.write(_json.dumps(tasks_file_content))

    # Run Gulp tasks
    debug = _reg.get('debug')
    _run_node_bin('gulp', '--silent', gulpfile=_GULPFILE, debug=debug, tasksFile=_GULP_TASKS_FILE)

    # Build RequireJS config file
    requirejs_paths = {}
    for m_name, m_location in _requirejs_modules.items():
        m_pkg_name, m_path = _split_location_info(m_location)
        requirejs_paths[m_name] = '{}/{}'.format(m_pkg_name, m_path)
    rjs_config = _tpl.render('pytsite.assetman@requirejs-config', {'paths': _json.dumps(requirejs_paths)})
    rjs_config_path = _path.join(assets_static_path, 'pytsite.assetman', 'require-config.js')
    rjs_config_dir = _path.dirname(rjs_config_path)
    if not _path.exists(rjs_config_dir):
        _makedirs(rjs_config_dir, 0o755, True)
    with open(rjs_config_path, 'wt') as f:
        f.write(rjs_config)

    _events.fire('pytsite.assetman.build')

    if maintenance:
        _maintenance.disable()


def _split_location_info(location: str) -> _Tuple[str, str]:
    """Split asset path into package name and asset path.
    """
    if '@' not in location:
        location = '$theme@' + location

    if '$theme' in location:
        location = location.replace('$theme', _theme.get().package_name)

    package_name, assets_path = location.split('@')[:2]

    return resolve_package_name(package_name), assets_path
