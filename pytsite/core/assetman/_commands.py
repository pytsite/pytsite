"""Assetman Console Commands
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from os import path, walk, makedirs
from shutil import rmtree, copy
from webassets import Environment, Bundle
from webassets.script import CommandLineEnvironment
from pytsite.core import reg, logger
from pytsite.core.lang import t
from pytsite.core.console import AbstractConsoleCommand, print_info, run_console_command
from ._functions import get_packages


class BuildAssets(AbstractConsoleCommand):
    def get_name(self) -> str:
        return 'assetman:build'

    def get_description(self) -> str:
        return t('pytsite.core@assetman_console_command_description')

    def execute(self, **kwargs: dict):
        """Compile assets.
        """
        static_dir = reg.get('paths.static')
        debug = reg.get('debug.enabled')

        if path.exists(static_dir):
            rmtree(static_dir)

        for pkg_name, package_assets_dir in get_packages().items():
            # Building package's assets absolute paths list
            files_list = []
            for root, dirs, files in walk(package_assets_dir):
                for file in files:
                    files_list.append(path.join(root, file))

            for src in files_list:
                if '.webassets-cache' in src:
                    continue

                dst = src.replace(package_assets_dir + path.sep, '')
                dst = path.join(static_dir, 'assets', pkg_name, dst)

                ext = path.splitext(src)[1]
                if ext in ['.js', '.css', '.less']:
                    filters = []

                    if ext == '.less':
                        filters.append('less')
                        dst = re.sub(r'\.less$', '.css', dst)
                        ext = '.css'

                    if ext == '.js' and reg.get('output.minify') and not src.endswith('.min.js'):
                        filters.append('rjsmin')

                    if ext == '.css' and reg.get('output.minify') and not src.endswith('.min.css'):
                        filters.append('cssutils')

                    bundle = Bundle(src, filters=filters)
                    env = Environment(directory=package_assets_dir, debug=debug, versions=False,
                                      manifest=False, cache=False)
                    env.register('bundle', bundle, output=dst)

                    print_info('Compiling {} -> {}'.format(src, dst))
                    cmd = CommandLineEnvironment(env, logger)
                    cmd.invoke('build', {})
                elif '.webassets-cache' not in src:
                    dst_dir = path.dirname(dst)
                    if not path.exists(dst_dir):
                        makedirs(dst_dir, 0o755)
                    copy(src, dst)

        run_console_command('lang:build')
