# Public API
import jinja2 as _jinja
from datetime import datetime as _datetime
from importlib import import_module as _import_module
from os import path as _path
from urllib.parse import urlparse as _urlparse
from pytsite import reg as _reg, lang as _lang, util as _util, events as _events
from . import _error as error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_packages = {}


def _get_tpl_path(tpl: str) -> str:
    if not tpl:
        raise ValueError('Template name is not specified.')

    package_name = 'app'
    tpl_split = tpl.split('@')
    if len(tpl_split) == 2:
        package_name = tpl_split[0]
        tpl = tpl_split[1]

    if package_name not in _packages:
        raise error.TemplateNotFound("Package {} is not registered.".format(package_name))

    if not tpl.endswith('.jinja2'):
        tpl += '.jinja2'

    return _path.join(_packages[package_name]['templates_dir'], tpl)


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


def register_package(package_name: str, templates_dir: str = 'res/tpl'):
    """Register templates container.
    """
    if package_name in _packages:
        raise Exception("Package '{}' already registered.".format(package_name))

    package = _import_module(package_name)
    templates_dir = _path.join(_path.abspath(_path.dirname(package.__file__)), templates_dir)
    if not _path.isdir(templates_dir):
        raise FileNotFoundError("Directory '{}' is not found.".format(templates_dir))

    _packages[package_name] = {'templates_dir': templates_dir}


def render(template: str, args: dict = None) -> str:
    """Render a template.
    """
    if not args:
        args = {}

    _events.fire('pytsite.tpl.render', args=args)

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
