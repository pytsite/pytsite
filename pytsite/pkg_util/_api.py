"""PytSite Package Utilities API
"""
import re as _re
import json as _json
from typing import List as _List
from importlib.util import find_spec as _find_module_spec
from os import path as _path
from pytsite import semver as _semver
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_REQUIREMENT_DEF_RE = _re.compile('([a-zA-Z0-9_]+)(==|!=|<|>|<=|>=)(\d+\.\d+\.\d+|\d+\.\d+|\d+)')
_parsed_json = {}


def resolve_path(package_name: str):
    # Check for package existence
    spec = _find_module_spec(package_name)
    if not spec or not spec.loader:
        raise FileNotFoundError("Package '{}' is not found".format(package_name))

    package_path = _path.dirname(spec.origin)
    if not _path.isdir(package_path):
        raise FileNotFoundError("'{}' is not a directory".format(package_path))

    return package_path


def parse_json(package_name: str, json_name: str = None) -> dict:
    if not json_name:
        json_name = 'pytsite-package.json'
        if package_name == 'pytsite':
            json_name = 'pytsite.json'
        if package_name == 'app':
            json_name = 'app.json'
        elif package_name.startswith('themes.'):
            json_name = 'theme.json'
        elif package_name.startswith('plugins.'):
            json_name = 'plugin.json'

    json_path = _path.join(resolve_path(package_name), json_name)

    if json_path in _parsed_json:
        return _parsed_json[json_path]

    if not _path.isfile(json_path):
        raise FileNotFoundError("'{}' is not found".format(json_path))

    try:
        with open(json_path) as f:
            json_data = _json.load(f)
    except _json.JSONDecodeError as e:
        raise _json.JSONDecodeError("Error while loading JSON data from '{}': {}".format(json_path, e), e.doc, e.pos)

    if not isinstance(json_data, dict):
        raise TypeError("'{}' should contain a valid JSON object".format(json_path))

    _parsed_json[json_path] = json_data

    return json_data


def data(package_name: str, key: str, default=None, json_name: str = None):
    return parse_json(package_name, json_name).get(key, default)


def name(package_name: str, json_name: str = None) -> str:
    """Shortcut
    """
    return data(package_name, 'name', '', json_name)


def version(package_name: str, json_name: str = None) -> str:
    """Shortcut
    """
    return data(package_name, 'version', '', json_name)


def description(package_name: str, json_name: str = None) -> str:
    """Shortcut
    """
    return data(package_name, 'description', '', json_name)


def requires(package_name: str, json_name: str = None) -> _List[str]:
    """Shortcut
    """
    r_str = data(package_name, 'requires', '', json_name)

    return r_str.replace(' ', '').split(',') if r_str else []


def author(package_name: str, json_name: str = None) -> str:
    """Shortcut
    """
    return data(package_name, 'author', '', json_name)


def author_email(package_name: str, json_name: str = None) -> str:
    """Shortcut
    """
    return data(package_name, 'author_email', '', json_name)


def url(package_name: str, json_name: str = None) -> str:
    """Shortcut
    """
    return data(package_name, 'url', '', json_name)


def license_name(package_name: str, json_name: str = None) -> str:
    """Shortcut
    """
    return data(package_name, 'license_name', '', json_name)


def check_requirements(package_name: str, json_name: str = None):
    """Check if installed packages have required versions

    Requirements string should be like 'pytsite >= 1.2.3, app <= 3.2.1, themes.default == 1.0', etc.
    Spaces are not significant.
    """
    for req in requires(package_name, json_name):
        match = _REQUIREMENT_DEF_RE.match(req)
        if not match:
            raise _error.InvalidRequirementString("'{}' is not a valid requirement string".format(req))

        try:
            required_package_name = match.group(1)
            condition = match.group(2) + match.group(3)
            installed_version = version(required_package_name)

            if not _semver.check_condition(installed_version, condition):
                raise _error.MissingRequiredVersion(package_name, required_package_name, condition, installed_version)

        except ImportError:
            raise _error.MissingRequiredPackage(package_name)
