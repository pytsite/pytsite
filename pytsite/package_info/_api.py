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
    req_packages = req.get('packages')
    if not (req_packages and isinstance(req_packages, list)):
        json_data['requires']['packages'] = []
    req_plugins = req.get('plugins')
    if not (req_plugins and isinstance(req_plugins, list)):
        json_data['requires']['plugins'] = []

    return json_data


def data(package_name_or_json_path: str, key: str = None, defaults: dict = None, override: dict = None) -> _Any:
    if package_name_or_json_path.startswith('/'):
        source = package_name_or_json_path
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
    if source in _parsed_json:
        d = _parsed_json[source]

    # Load and cache data
    else:
        try:
            d = parse_json(_util.load_json(source), defaults, override)
            _parsed_json[source] = d
        except ValueError as e:
            raise ValueError("Value error in '{}': {}".format(source, e))

    return d.get(key) if key else d


def name(package_name_or_json_path: str) -> str:
    """Shortcut
    """
    return data(package_name_or_json_path, 'name')


def version(package_name_or_json_path: str) -> str:
    """Shortcut
    """
    return str(_semver.parse_version_str(data(package_name_or_json_path, 'version')))


def description(package_name_or_json_path: str) -> dict:
    """Shortcut
    """
    return data(package_name_or_json_path, 'description')


def requires(package_name_or_json_path: str) -> _Dict[str, _List[str]]:
    """Shortcut
    """
    return data(package_name_or_json_path, 'requires')


def requires_packages(package_name_or_json_path: str) -> _List[str]:
    """Shortcut
    """
    return data(package_name_or_json_path, 'requires')['packages']


def requires_plugins(package_name_or_json_path: str) -> _List[str]:
    """Shortcut
    """
    return data(package_name_or_json_path, 'requires')['plugins']


def url(package_name_or_json_path: str) -> str:
    """Shortcut
    """
    return data(package_name_or_json_path, 'url')
