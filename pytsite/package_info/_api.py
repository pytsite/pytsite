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


def resolve_path(package_name: str):
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
    requires_packages = req.get('packages')
    if not (requires_packages and isinstance(requires_packages, list)):
        json_data['requires']['packages'] = []
    requires_plugins = req.get('plugins')
    if not (requires_plugins and isinstance(requires_plugins, list)):
        json_data['requires']['plugins'] = []

    return json_data


def data(package_name: str, key: str = None, defaults: dict = None, override: dict = None) -> _Any:
    if package_name == 'pytsite':
        json_name = 'pytsite.json'
    elif package_name == 'app':
        json_name = 'app.json'
    elif package_name.startswith('themes.'):
        json_name = 'theme.json'
    elif package_name.startswith('plugins.'):
        json_name = 'plugin.json'
    else:
        json_name = 'pytsite-package.json'

    # Calculate path to the JSON file
    source = _path.join(resolve_path(package_name), json_name)

    # Check cache
    if source in _parsed_json:
        d = _parsed_json[source]
    else:
        # Load, sanitize and cache JSON
        try:
            d = parse_json(_util.load_json(source), defaults, override)
            _parsed_json[source] = d
        except ValueError as e:
            raise ValueError("Value error in '{}': {}".format(source, e))

    return d.get(key) if key else d


def name(package_name: str) -> str:
    """Shortcut
    """
    return data(package_name, 'name')


def version(package_name: str) -> str:
    """Shortcut
    """
    return data(package_name, 'version')


def description(package_name: str) -> dict:
    """Shortcut
    """
    return data(package_name, 'description')


def requires(package_name: str) -> _Dict[str, _List[str]]:
    """Shortcut
    """
    return data(package_name, 'requires')


def requires_packages(package_name: str) -> _List[str]:
    """Shortcut
    """
    return data(package_name, 'requires')['packages']


def requires_plugins(package_name: str) -> _List[str]:
    """Shortcut
    """
    return data(package_name, 'requires')['plugins']


def url(package_name: str) -> str:
    """Shortcut
    """
    return data(package_name, 'url')


def check_requirements(package_name: str, auto_install: bool = False):
    """Check for requirements
    """
    from pytsite import plugman

    # Check for required pip packages
    for pip_pkg_requirement in requires(package_name)['packages']:
        pip_pkg_name, pip_pkg_ver_spec = _semver.parse_requirement_str(pip_pkg_requirement)
        try:
            installed_pip_pkg_info = _util.get_installed_pip_package_info(pip_pkg_name)
            if not _semver.check_conditions(installed_pip_pkg_info['version'], pip_pkg_ver_spec):
                err_msg = "Package '{}' requires pip package '{}{}', but '{}=={}' is installed".format(
                    package_name, pip_pkg_name, pip_pkg_ver_spec, pip_pkg_name, installed_pip_pkg_info['version']
                )
                raise _error.MissingRequiredPipPackageVersion(err_msg)

        except _util.error.PipPackageNotInstalled:
            if auto_install:
                _util.install_pip_package(pip_pkg_name, pip_pkg_ver_spec)
            else:
                raise _error.MissingRequiredPipPackage("Pip package '{}' is not installed".format(pip_pkg_requirement))

    # Check for required plugins
    for plugin_requirement in requires(package_name)['plugins']:
        plugin_name, plugin_ver_spec = _semver.parse_requirement_str(plugin_requirement)

        try:
            plugin_info = plugman.plugin_info(plugin_name)
        except plugman.error.PluginNotInstalled:
            if auto_install:
                plugman.install(plugin_requirement)

                # for req in requires(package_name):

                #
                #     try:
                #         required_package_name = match.group(1)
                #         condition = match.group(2) + match.group(3)
                #         installed_version = version(required_package_name)
                #
                #         if not _semver.check_conditions(installed_version, condition):
                #             raise _error.MissingRequiredVersion(package_name, required_package_name, condition, installed_version)
                #
                #     except ImportError:
                #         raise _error.MissingRequiredPackage(package_name)
