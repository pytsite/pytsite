from datetime import datetime as _datetime
from importlib import import_module as _import_module
from os import path as _path
import jinja2 as _jinja
from pytsite import metatag as _metatag, reg as _reg, assetman as _assetman, lang as _lang, browser as _browser, \
    util as _util
from pytsite import router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_packages = {}


class _TemplateLoader(_jinja.BaseLoader):
    """Template loader.
    """
    def get_source(self, environment, template: str)->tuple:
        if not template:
            raise TypeError('Template name is not specified.')

        package_name = 'app'
        template_split = template.split('@')
        if len(template_split) == 2:
            package_name = template_split[0]
            template = template_split[1]

        if package_name not in _packages:
            raise _jinja.TemplateNotFound("Package {} is not registered.".format(package_name))

        if not template.endswith('.jinja2'):
            template += '.jinja2'

        template_abs_path = _path.join(_packages[package_name]['templates_dir'], template)
        if not _path.exists(template_abs_path):
            raise _jinja.TemplateNotFound("Template is not found at '{}'.".format(template_abs_path))

        file = open(template_abs_path)
        source = file.read()
        file.close()

        mtime = _path.getmtime(template_abs_path)

        return source, template_abs_path, lambda: mtime == _path.getmtime(template_abs_path)


_env = _jinja.Environment(loader=_TemplateLoader(), extensions=['jinja2.ext.do'])


def _date_filter(value: _datetime, fmt: str='pretty_date') -> str:
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


# Additional functions and filters
_env.globals['lang'] = _lang
_env.globals['t'] = _lang.t
_env.globals['t_plural'] = _lang.t_plural
_env.globals['reg'] = _reg
_env.globals['router'] = _router
_env.globals['url'] = _router.url
_env.globals['ep_url'] = _router.ep_url
_env.globals['current_url'] = _router.current_url
_env.globals['base_url'] = _router.base_url
_env.globals['is_base_url'] = _router.is_base_url
_env.globals['nav_link'] = _util.nav_link
_env.globals['asset_url'] = _assetman.get_url
_env.globals['metatag'] = _metatag
_env.globals['assetman'] = _assetman
_env.globals['browser'] = _browser
_env.filters['date'] = _date_filter
_env.filters['nl2br'] = _nl2br_filter


def register_package(package_name: str, templates_dir: str='res/tpl'):
    """Register templates container.
    """
    if package_name in _packages:
        raise Exception("Package '{}' already registered.".format(package_name))

    package = _import_module(package_name)
    templates_dir = _path.join(_path.abspath(_path.dirname(package.__file__)), templates_dir)
    if not _path.isdir(templates_dir):
        raise FileNotFoundError("Directory '{}' is not found.".format(templates_dir))

    _packages[package_name] = {'templates_dir': templates_dir}


def render(template: str, data: dict=None) -> str:
    """Render a template.
    """
    if not data:
        data = {}

    return _env.get_template(template).render(data)


def register_global(name: str, obj):
    """Register global.
    """
    _env.globals[name] = obj
