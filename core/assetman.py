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
    assets_abs_dir = path.join(path.dirname(spec.origin), assets_dir)
    if not path.isdir(assets_abs_dir):
        raise Exception("Directory '{0}' is not exists.".format(assets_abs_dir))

    __packages[package_name] = {
        'path': assets_dir,
        'assets': {'js': [], 'compressed_js': [], 'css': [], 'compressed_css': [], 'other': []},
    }


def add(path: str):
    """Add an asset.
    """
    package_name, asset_path, bundle_name = __split_asset_path_info(path)

    assets_list = __packages[package_name]['assets'][bundle_name]
    assets_list.append(asset_path)


def url(path: str)->str:
    """Get URL of an asset.
    """
    package_name, asset_path, bundle_name = __split_asset_path_info(path)
    assets_list = __packages[package_name]['assets'][bundle_name]
    if asset_path not in assets_list:
        raise Exception("Asset '{0}' is not defined in package '{1}'.".format(asset_path, package_name))

    asset_path = '/assets/{0}/{1}'.format(package_name, asset_path)

    from . import router
    return router.url(asset_path, strip_language_part=True)


def __split_asset_path_info(path: str)->dict:
    """Split asset path into package name and asset path.
    """
    path_parts = path.split('@')
    package_name = 'app'
    asset_path = path
    if len(path_parts) == 2:
        package_name = path_parts[0]
        asset_path = path_parts[1]

    if package_name not in __packages:
        raise Exception("Package '{0}' is not registered.".format(package_name))

    if asset_path.endswith('.js'):
        bundle_name = 'js'
    elif asset_path.endswith('.min.js'):
        bundle_name = 'compressed_js'
    elif asset_path.endswith('.css'):
        bundle_name = 'css'
    elif asset_path.endswith('.min.css'):
        bundle_name = 'compressed_css'
    else:
        bundle_name = 'other'

    return package_name, asset_path, bundle_name