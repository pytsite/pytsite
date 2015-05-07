__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

__packages = {}


def register_package(package_name: str, assets_dir: str='assets'):
    """Register assets container.
    """
    from importlib.util import find_spec
    spec = find_spec(package_name)
    if not spec:
        raise Exception("Package '{0}' is not found.".format(package_name))

    from os import path
    assets_dir = path.join(path.dirname(spec.origin), assets_dir)
    if not path.isdir(assets_dir):
        raise Exception("Directory '{0}' is not exists.".format(assets_dir))

    from webassets import Bundle
    __packages[package_name] = {
        '_path': assets_dir,  # absolute path to the package's assets dir
        '_bundle': Bundle(),  # weassets' bundle
    }


def add(path: str):
    path_parts = path.split('@')
    package_name = 'app'
    asset_path = path
    if len(path_parts) == 2:
        package_name = path_parts[0]
        asset_path = path_parts[1]

    if package_name not in __packages:
        raise Exception("Package '{0}' is not registered.".format(package_name))

    bundle = __packages[package_name]['_bundle']
    bundle.contents.append(asset_path)

    print(package_name)
    print(asset_path)