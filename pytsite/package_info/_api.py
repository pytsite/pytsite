"""PytSite Package Utilities API
"""
import json as _json
from typing import List as _List, Any as _Any, Dict as _Dict, Union as _Union
from importlib.util import find_spec as _find_module_spec
from os import path as _path
from pytsite import semver as _semver, util as _util
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_parsed_json = {}


def resolve_package_path(package_name: str):
    """Check for package existence
    """
    spec = _find_module_spec(package_name)
    if not spec or not spec.loader:
        raise _error.PackageNotFound("Package '{}' is not found".format(package_name))

    package_path = _path.dirname(spec.origin)
    if not _path.isdir(package_path):
        raise _error.PackageNotFound("'{}' is not a directory".format(package_path))

    return package_path


def parse_json(json_data: _Union[str, dict, list], defaults: dict = None, override: dict = None) -> dict:
    """Parse package's JSON from string
    """
    from pytsite import lang as _lang

    # Check data type
    if isinstance(json_data, str):
        json_data = _json.loads(json_data)
    if not isinstance(json_data, dict):
        raise TypeError('Data should be a valid JSON')

    # Set defaults
    if defaults is None:
        defaults = {}

    # Override data
    if isinstance(override, dict):
        json_data = _util.dict_merge(json_data, override)

    # Check name
    pkg_name = json_data.setdefault('name', defaults.get('name'))
    if not (pkg_name and isinstance(pkg_name, str)):
        raise ValueError("'name' is not found")

    # Check version
    pkg_version = json_data.setdefault('version', defaults.get('version'))
    if not (pkg_version and isinstance(pkg_version, str)):
        raise ValueError("'version' is not found")

    # Check URL
    pkg_url = json_data.setdefault('url', defaults.get('url'))
    if not (pkg_url and isinstance(pkg_url, str)):
        json_data['url'] = 'https://plugins.pytsite.xyz'

    # Check description
    pkg_desc = json_data.setdefault('description', defaults.get('description'))
    if not (pkg_desc and isinstance(pkg_desc, dict)):
        json_data['description'] = pkg_desc = {}

    # Check description translations
    for lng in _lang.langs():
        t_description = pkg_desc.get(lng)
        if not (t_description and isinstance(t_description, str)):
            json_data['description'][lng] = ''

    # Check author
    pkg_author = json_data.setdefault('author', defaults.get('author'))
    if not (pkg_author and isinstance(pkg_author, dict)):
        json_data['author'] = pkg_author = {}
    if not pkg_author.get('name'):
        json_data['author']['name'] = 'PytSite'
    if not pkg_author.get('email'):
        json_data['author']['email'] = 'info@pytsite.xyz'
    if not pkg_author.get('url'):
        json_data['author']['url'] = 'https://plugins.pytsite.xyz'

    # Check license info
    pkg_license = json_data.setdefault('license', defaults.get('license'))
    if not (pkg_license and isinstance(pkg_license, dict)):
        json_data['license'] = pkg_license = {}
    if not pkg_license.get('name'):
        json_data['license']['name'] = 'MIT'
    if not pkg_license.get('url'):
        json_data['license']['url'] = 'https://opensource.org/licenses/MIT'

    # Check requirements
    req = json_data.setdefault('requires', defaults.get('requires'))
    if not (req and isinstance(req, dict)):
        json_data['requires'] = req = {'packages': [], 'plugins': []}
    req_pytsite = req.get('pytsite')
    if not (req_pytsite and isinstance(req_pytsite, str)):
        json_data['requires']['pytsite'] = '>=0.0.1'
    req_packages = req.get('packages')
    if not (req_packages and isinstance(req_packages, list)):
        json_data['requires']['packages'] = []
    req_plugins = req.get('plugins')
    if not (req_plugins and isinstance(req_plugins, list)):
        json_data['requires']['plugins'] = []

    return json_data


def data(package_name_or_json_path: str, key: str = None, defaults: dict = None, override: dict = None,
         use_cache: bool = True) -> _Any:
    if package_name_or_json_path.startswith('/'):
        source = package_name_or_json_path
        if not _path.exists(source):
            raise _error.PackageNotFound()
    else:
        if package_name_or_json_path == 'pytsite':
            json_name = 'pytsite.json'
        elif package_name_or_json_path == 'app':
            json_name = 'app.json'
        elif package_name_or_json_path.startswith('themes.'):
            json_name = 'theme.json'
        elif package_name_or_json_path.startswith('plugins.'):
            json_name = 'plugin.json'
        else:
            json_name = 'pytsite-package.json'

        # Calculate path to the JSON file
        source = _path.join(resolve_package_path(package_name_or_json_path), json_name)

    # Get data from cache if available
    if use_cache and source in _parsed_json:
        d = _parsed_json[source]

    # Load and cache data
    else:
        try:
            d = parse_json(_util.load_json(source), defaults, override)
            if use_cache:
                _parsed_json[source] = d
        except ValueError as e:
            raise ValueError("Value error in '{}': {}".format(source, e))

    return d.get(key) if key else d


def name(package_name_or_json_path: str, use_cache: bool = True) -> str:
    """Shortcut
    """
    return data(package_name_or_json_path, 'name', use_cache=use_cache)


def version(package_name_or_json_path: str, use_cache: bool = True) -> str:
    """Shortcut
    """
    return str(_semver.parse_version_str(data(package_name_or_json_path, 'version', use_cache=use_cache)))


def description(package_name_or_json_path: str, use_cache: bool = True) -> dict:
    """Shortcut
    """
    return data(package_name_or_json_path, 'description', use_cache=use_cache)


def requires(package_name_or_json_path: str, use_cache: bool = True) -> _Dict[str, _List[str]]:
    """Shortcut
    """
    return data(package_name_or_json_path, 'requires', use_cache=use_cache)


def requires_pytsite(package_name_or_json_path: str, use_cache: bool = True) -> str:
    """Shortcut
    """
    return data(package_name_or_json_path, 'requires', use_cache=use_cache)['pytsite']


def requires_packages(package_name_or_json_path: str, use_cache: bool = True) -> _List[str]:
    """Shortcut
    """
    return data(package_name_or_json_path, 'requires', use_cache=use_cache)['packages']


def requires_plugins(package_name_or_json_path: str, use_cache: bool = True) -> _List[str]:
    """Shortcut
    """
    return data(package_name_or_json_path, 'requires', use_cache=use_cache)['plugins']


def url(package_name_or_json_path: str, use_cache: bool = True) -> str:
    """Shortcut
    """
    return data(package_name_or_json_path, 'url', use_cache=use_cache)


def check_requirements(pkg_name: str):
    from pytsite import pip, plugman

    # Check for required PytSite version
    req_ps_ver = requires_pytsite(pkg_name)
    if not _semver.check_conditions(version('pytsite'), req_ps_ver):
        req_ps_cond = _semver.parse_condition_str(req_ps_ver)
        raise _error.RequiredPytSiteVersionNotInstalled("{}{}".format(req_ps_cond[0], str(req_ps_cond[1])))

    # Check for required pip packages
    for req_pkg_spec in requires_packages(pkg_name):
        if not pip.is_installed(req_pkg_spec):
            req_pkg_cond = _semver.parse_requirement_str(req_pkg_spec)
            raise _error.RequiredPipPackageNotInstalled('{}{}'.format(req_pkg_cond[0], req_pkg_cond[1]))

    # Check for required plugins
    for req_plugin_spec in requires_plugins(pkg_name):
        if not plugman.is_installed(req_plugin_spec):
            req_plugin_cond = _semver.parse_requirement_str(req_plugin_spec)
            raise _error.RequiredPluginNotInstalled('{}{}'.format(req_plugin_cond[0], req_plugin_cond[1]))
