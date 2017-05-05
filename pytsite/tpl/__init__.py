# Public API
import jinja2 as _jinja
from datetime import datetime as _datetime
from importlib.util import find_spec as _find_module_spec
from os import path as _path
from urllib.parse import urlparse as _urlparse
from pytsite import reg as _reg, lang as _lang, util as _util, events as _events, theme as _theme
from . import _error as error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_packages = {}


def _get_tpl_path(tpl: str) -> str:
    if not tpl:
        raise ValueError('Template name is not specified.')

    if '@' not in tpl:
        tpl = '$theme@' + tpl

    if '$theme' in tpl:
        tpl = tpl.replace('$theme', _theme.get().name)

    package_name, tpl_name = tpl.split('@')[:2]

    if package_name not in _packages:
        raise error.TemplateNotFound("Templates package '{}' is not registered.".format(package_name))

    if not tpl_name.endswith('.jinja2'):
        tpl_name += '.jinja2'

    return _path.join(_packages[package_name]['templates_dir'], tpl_name)


def tpl_exists(tpl: str) -> bool:
    return _path.exists(_get_tpl_path(tpl))


class _TemplateLoader(_jinja.BaseLoader):
    """Template loader.
    """

    def get_source(self, environment, tpl: str) -> tuple:
        tpl_path = _get_tpl_path(tpl)

        if not tpl_exists(tpl):
            raise error.TemplateNotFound("Template is not found at '{}'.".format(tpl_path))

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


def _nl2br_filter(value: str) -> str:
    return value.replace('\n', _jinja.Markup('<br>'))


def is_package_registered(package_name: str):
    """Check if the package already registered.
    """
    return package_name in _packages


def register_package(package_name: str, templates_dir: str = 'res/tpl', alias: str = None):
    """Register templates container.
    """
    if package_name in _packages:
        raise RuntimeError("Package '{}' already registered.".format(package_name))

    pkg_spec = _find_module_spec(package_name)
    if not pkg_spec:
        raise RuntimeError("Package '{}' is not found".format(package_name))

    templates_dir = _path.join(_path.dirname(pkg_spec.origin), templates_dir)
    if not _path.isdir(templates_dir):
        raise NotADirectoryError("Directory '{}' is not found".format(templates_dir))

    config = {'templates_dir': templates_dir}
    if alias:
        _packages[alias] = config
    else:
        _packages[package_name] = config


def render(template: str, args: dict = None) -> str:
    """Render a template.
    """
    if not args:
        args = {}

    _events.fire('pytsite.tpl.render', tpl_name=template, args=args)

    return _env.get_template(template).render(args)


def is_global_registered(name: str) -> bool:
    """Check if the global registered.
    """
    return name in _env.globals


def register_global(name: str, obj):
    """Register global.
    """
    _env.globals[name] = obj


# Additional functions and filters
_env.globals['t'] = _lang.t
_env.globals['t_plural'] = _lang.t_plural
_env.globals['current_lang'] = _lang.get_current
_env.globals['reg_get'] = _reg.get
_env.globals['nav_link'] = _util.nav_link
_env.globals['url_parse'] = _urlparse
_env.filters['date'] = _date_filter
_env.filters['nl2br'] = _nl2br_filter
