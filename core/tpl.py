from jinja2 import Environment as _Environment, PackageLoader as _PackageLoader

_loaders = {}
_env = _Environment()


def register_package(package_name: str, templates_dir: str='tpl'):
    if package_name not in _loaders:
        _loaders[package_name] = _PackageLoader(package_name, templates_dir)


def render(package_name: str, tpl_name: str, data: dict):
    """Render a template.
    """
    if package_name not in _loaders:
        raise Exception("Package '{0}' is not registered as template container.".format(package_name))

    # Switch loader
    _env.loader = _loaders[package_name]

    return _env.get_template(tpl_name).render(data)