__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from . import console
from .lang import t


class ConsoleCommand(console.Command):
    def get_name(self)->str:
        return 'assetman:build'

    def get_description(self)->str:
        return t('pytsite.core@assetman_console_command_description')

    def execute(self, args: dict):
        compile_assets()


console.register_command(ConsoleCommand())

__packages = {}


def register_package(package_name: str, assets_dir: str='assets', languages_dir='lng'):
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

    __packages[package_name] = {
        'assets_dir': assets_dir,
    }


def url(path: str)->str:
    """Get URL of an asset.
    """
    package_name, asset_path, bundle_name = __split_asset_path_info(path)
    assets_list = __packages[package_name]['assets'][bundle_name]
    if asset_path not in assets_list:
        raise Exception("Asset '{0}' is not defined in package '{1}'.".format(asset_path, package_name))

    from . import router
    return router.url('/assets/{0}/{1}'.format(package_name, asset_path), strip_language_part=True)


def compile_assets():
    """Compile assets.
    """
    import os
    from shutil import rmtree, copy
    from webassets import Environment
    from webassets.script import CommandLineEnvironment
    from . import registry, application

    static_dir = registry.get_val('paths.static')
    debug = registry.get_val('debug.enabled')

    if os.path.exists(static_dir):
        rmtree(static_dir)

    for pkg_name in __packages:
        # Building package's assets absolute paths list
        package_assets_dir = __packages[pkg_name]['assets_dir']
        files_list = []
        for root, dirs, files in os.walk(package_assets_dir):
            for file in files:
                files_list.append(os.path.join(root, file))

        for src in files_list:
            if '.webassets-cache' in src:
                continue

            dst = src.replace(package_assets_dir + os.path.sep, '')
            dst = os.path.join(static_dir, 'assets', pkg_name, dst)
            print('Compiling {0} -> {1}'.format(src, dst))

            ext = os.path.splitext(src)[1]
            if ext in ['.js', '.css']:
                filters = None

                if ext == '.js' and not src.endswith('.min.js'):
                    filters = 'rjsmin'

                if ext == '.css' and not src.endswith('.min.css'):
                    filters = 'cssutil'

                env = Environment(directory=package_assets_dir, filters=filters, debug=debug)
                env.register('bundle', src, output=dst)
                cmd = CommandLineEnvironment(env, application.logger())
                cmd.invoke('build', dict())
            elif '.webassets-cache' not in src:
                dst_dir = os.path.dirname(dst)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir, 0o755)
                copy(src, dst)


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

    return package_name, asset_path