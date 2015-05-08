from jinja2 import Environment as _Environment, PackageLoader as _PackageLoader
from . import lang, metatag
from .helpers import dd

__loaders = {}
__env = _Environment()


# Translate function
__env.globals['t'] = lang.translate
__env.globals['meta_tags'] = metatag.dump_all


def register_package(package_name: str, templates_dir: str='tpl'):
    """Register templates container.
    """
    if package_name not in __loaders:
        __loaders[package_name] = _PackageLoader(package_name, templates_dir)


def render(tpl_location: str, data: dict=None)->str:
    """Render a template.
    """
    package_name = 'app'
    tpl_name = tpl_location
    tpl_location_splitted = tpl_location.split('@')
    if len(tpl_location_splitted) == 2:
        package_name = tpl_location_splitted[0]
        tpl_name = tpl_location_splitted[1]

    if package_name not in __loaders:
        raise Exception("Package '{0}' is not registered as template container.".format(package_name))

    # Switch loader
    __env.loader = __loaders[package_name]

    return __env.get_template(tpl_name).render(data)
