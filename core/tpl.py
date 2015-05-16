__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from importlib import import_module
from os import path
from jinja2 import Environment, BaseLoader, TemplateNotFound
from . import router, lang, metatag, reg, assetman

_packages = dict()


class TemplateLoader(BaseLoader):
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
            raise TemplateNotFound("Package {0} is not registered.".format(package_name))

        if not template.endswith('.jinja2'):
            template += '.jinja2'

        template_abs_path = path.join(_packages[package_name]['templates_dir'], template)
        if not path.exists(template_abs_path):
            raise TemplateNotFound("Template is not found at '{0}'.".format(template_abs_path))

        file = open(template_abs_path)
        source = file.read()
        file.close()

        mtime = path.getmtime(template_abs_path)

        return source, template_abs_path, lambda: mtime == path.getmtime(template_abs_path)


__env = Environment(loader=TemplateLoader(), extensions=['jinja2.ext.do'])


# Additional functions
__env.globals['lang'] = lang
__env.globals['t'] = lang.translate
__env.globals['reg'] = reg
__env.globals['router'] = router
__env.globals['metatag'] = metatag
__env.globals['assetman'] = assetman


def register_package(package_name: str, templates_dir: str='tpl'):
    """Register templates container.
    """
    if package_name in _packages:
        raise Exception("Package '{0}' already registered.".format(package_name))

    package = import_module(package_name)
    templates_dir = path.join(path.abspath(path.dirname(package.__file__)), templates_dir)
    if not path.isdir(templates_dir):
        raise FileNotFoundError("Directory '{0}' is not found.".format(templates_dir))

    _packages[package_name] = {'templates_dir': templates_dir}


def render(template: str, data: dict=None)->str:
    """Render a template.
    """
    if not data:
        data = dict()
    return __env.get_template(template).render(data)
