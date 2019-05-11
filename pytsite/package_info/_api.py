"""PytSite Package Utilities API
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re as _re
import json as _json
from typing import List as _List, Any as _Any, Dict as _Dict, Union as _Union
from importlib.util import find_spec as _find_module_spec
from os import path as _path
from pytsite import semver as _semver, util as _util
from . import _error

_REQ_RE = _re.compile('([a-zA-Z0-9\-_]+)\s*(.+)?')

_parsed_json = {}


def _sanitize_req(reqs: _Union[dict, list]) -> _Dict[str, _semver.VersionRange]:
    # Old versions can contain lists instead of dicts
    if isinstance(reqs, list):
        n_reqs = {}
        for req in reqs:
            match = _REQ_RE.findall(req)
            if not match:
                raise ValueError("Invalid requirement specification: '{}'".format(req))

            n_reqs[match[0][0]] = match[0][1]

        reqs = n_reqs

    # Convert version strings to VersionRange objects
    for n, v in reqs.items():
        reqs[n] = _semver.VersionRange(v)

    return reqs


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


def parse_json(json_data: _Union[str, dict, list], defaults: dict = None) -> dict:
    """Parse package's JSON from string
    """
    from pytsite import lang as _lang

    # Load data
    if isinstance(json_data, str):
        json_data = _json.loads(json_data)

    # Check data type
    if not isinstance(json_data, dict):
        raise TypeError('Dict expected, got {}'.format(type(json_data)))

    # Check defaults
    if defaults is None:
        defaults = {}

    # Check name
    pkg_name = json_data.setdefault('name', defaults.get('name'))
    if not (pkg_name and isinstance(pkg_name, str)):
        json_data['name'] = 'Untitled'

    # Check version
    pkg_ver = json_data.setdefault('version', _semver.Version(defaults.get('version', '0.0.1')))
    if not isinstance(pkg_ver, _semver.Version):
        json_data['version'] = _semver.Version(pkg_ver)

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
        json_data['requires'] = req = {'pytsite': None, 'packages': {}, 'plugins': {}}

    # Check required pytsite version
    json_data['requires']['pytsite'] = _semver.VersionRange(req.get('pytsite', '>=0.0.1'))

    # Check required pip packages versions
    json_data['requires']['packages'] = _sanitize_req(req.get('packages', {}))

    # Check required plugins versions
    json_data['requires']['plugins'] = _sanitize_req(req.get('plugins', {}))

    return json_data


def data(package_name_or_json_path: str, key: str = None, use_cache: bool = True, defaults: dict = None) -> _Any:
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
            d = parse_json(_util.load_json(source), defaults)
            if use_cache:
                _parsed_json[source] = d
        except ValueError as e:
            raise ValueError("Value error in '{}': {}".format(source, e))

    return d.get(key) if key else d


def name(package_name_or_json_path: str, use_cache: bool = True) -> str:
    """Shortcut
    """
    return data(package_name_or_json_path, 'name', use_cache)


def version(package_name_or_json_path: str, use_cache: bool = True) -> _semver.Version:
    """Shortcut
    """
    return data(package_name_or_json_path, 'version', use_cache)


def description(package_name_or_json_path: str, use_cache: bool = True) -> dict:
    """Shortcut
    """
    return data(package_name_or_json_path, 'description', use_cache)


def requires(package_name_or_json_path: str, use_cache: bool = True) -> _Dict[str, _List[str]]:
    """Shortcut
    """
    return data(package_name_or_json_path, 'requires', use_cache)


def requires_pytsite(package_name_or_json_path: str, use_cache: bool = True) -> str:
    """Shortcut
    """
    return data(package_name_or_json_path, 'requires', use_cache)['pytsite']


def requires_packages(package_name_or_json_path: str, use_cache: bool = True) -> _Dict[str, str]:
    """Shortcut
    """
    return data(package_name_or_json_path, 'requires', use_cache)['packages']


def requires_plugins(package_name_or_json_path: str, use_cache: bool = True) -> _Dict[str, str]:
    """Shortcut
    """
    return data(package_name_or_json_path, 'requires', use_cache)['plugins']


def url(package_name_or_json_path: str, use_cache: bool = True) -> str:
    """Shortcut
    """
    return data(package_name_or_json_path, 'url', use_cache)


def check_requirements(pkg_name: str):
    from pytsite import pip, plugman

    # Check for required PytSite version
    required_pytsite_ver = requires_pytsite(pkg_name)
    if version('pytsite') not in _semver.VersionRange(required_pytsite_ver):
        raise _error.RequiredPytSiteVersionNotInstalled(required_pytsite_ver)

    # Check for required pip packages
    for req_p_name, req_p_ver in requires_packages(pkg_name).items():
        if not pip.is_installed(req_p_name, _semver.VersionRange(req_p_ver)):
            raise _error.RequiredPipPackageNotInstalled('{}{}'.format(req_p_name, req_p_ver))

    # Check for required plugins
    for req_p_name, req_p_ver in requires_plugins(pkg_name).items():
        if not plugman.is_installed(req_p_name, _semver.VersionRange(req_p_ver)):
            raise _error.RequiredPluginNotInstalled('{}{}'.format(req_p_name, req_p_ver))
