"""PytSite Tpl
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
import jinja2 as _jinja
import json as _json
from typing import Mapping as _Mapping
from datetime import datetime as _datetime
from importlib.util import find_spec as _find_module_spec
from os import path as _path
from urllib.parse import urlparse as _urlparse
from pytsite import reg as _reg, lang as _lang, util as _util, events as _events, package_info as _package_info
from . import _error as error

_packages = {}


def _resolve_location(location: str) -> list:
    for r in _events.fire('pytsite.tpl@resolve_location', location=location):
        location = r

    if '@' in location:
        return location.split('@')[:2]
    else:
        return ['app', location]


def _resolve_name(tpl_name: str) -> str:
    for r in _events.fire('pytsite.tpl@resolve_name', tpl_name=tpl_name):
        tpl_name = r or tpl_name

    return tpl_name


def _get_path(location: str) -> str:
    if not location:
        raise ValueError('Template name is not specified')

    package_name, tpl_name = _resolve_location(location)

    if package_name not in _packages:
        raise error.TemplateNotFound("Templates package '{}' is not registered".format(package_name))

    if not tpl_name.endswith('.jinja2'):
        tpl_name += '.jinja2'

    return _path.join(_packages[package_name]['templates_dir'], tpl_name)


def tpl_exists(tpl: str) -> bool:
    return _path.exists(_get_path(tpl))


class _TemplateLoader(_jinja.BaseLoader):
    """Template loader.
    """

    def get_source(self, environment, tpl: str) -> tuple:
        tpl_path = _get_path(tpl)

        if not tpl_exists(tpl):
            raise error.TemplateNotFound("Template is not found at '{}'".format(tpl_path))

        with open(tpl_path, encoding='utf-8') as f:
            source = f.read()

        return source, tpl_path, lambda: False


_env = _jinja.Environment(loader=_TemplateLoader(), extensions=['jinja2.ext.do'])


def _date_filter(value: _datetime, fmt: str = 'pretty_date') -> str:
    if not value:
        value = _datetime.now()

    if fmt == 'pretty_date':
        return _lang.pretty_date(value)
    elif fmt == 'pretty_date_time':
        return _lang.pretty_date_time(value)
    else:
        return value.strftime(fmt)


def is_package_registered(package_name: str):
    """Check if the package already registered.
    """
    return package_name in _packages


def register_package(package_name: str, templates_dir: str = 'res/tpl', alias: str = None):
    """Register templates container.
    """
    if package_name in _packages:
        raise RuntimeError("Package '{}' already registered".format(package_name))

    pkg_spec = _find_module_spec(package_name)
    if not pkg_spec:
        raise RuntimeError("Package '{}' is not found".format(package_name))

    templates_dir = _path.join(_path.dirname(pkg_spec.origin), templates_dir)
    if not _path.isdir(templates_dir):
        raise NotADirectoryError("Directory '{}' is not found".format(templates_dir))

    if package_name.startswith('plugins.') and not alias:
        alias = package_name.split('.')[1]

    config = {'templates_dir': templates_dir}
    _packages[package_name] = config

    if alias:
        _packages[alias] = config


def render(template: str, args: _Mapping = None, emit_event: bool = True) -> str:
    """Render a template
    """
    if not args:
        args = {}

    if emit_event:
        _events.fire('pytsite.tpl@render', tpl_name=template, args=args)

    return _env.get_template(template).render(args)


def on_render(handler, priority: int = 0):
    """Shortcut function to register event handler
    """
    _events.listen('pytsite.tpl@render', handler, priority)


def is_global_registered(name: str) -> bool:
    """Check if the global registered.
    """
    return name in _env.globals


def register_global(name: str, obj):
    """Register global.
    """
    _env.globals[name] = obj


def on_resolve_location(handler, priority: int = 0):
    """Shortcut
    """
    _events.listen('pytsite.tpl@resolve_location', handler, priority)


def on_resolve_name(handler, priority: int = 0):
    """Shortcut
    """
    _events.listen('pytsite.tpl@resolve_name', handler, priority)


# Additional functions and filters
_env.globals['tpl_exists'] = tpl_exists
_env.globals['t'] = _lang.t
_env.globals['t_plural'] = _lang.t_plural
_env.globals['current_lang'] = _lang.get_current
_env.globals['reg_get'] = _reg.get
_env.globals['nav_link'] = _util.nav_link
_env.globals['url_parse'] = _urlparse
_env.globals['app_name'] = lambda: _reg.get('app.app_name_' + _lang.get_current(), 'PytSite')
_env.globals['app_version'] = _package_info.version('app')
_env.filters['date'] = _date_filter
_env.filters['nl2br'] = lambda value: value.replace('\n', _jinja.Markup('<br>'))
_env.filters['tojson'] = lambda obj: _json.dumps(obj)
