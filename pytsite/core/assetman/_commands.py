"""Assetman Console Commands.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from os import path as _path, walk as _walk, makedirs as _makedirs
from shutil import rmtree, copy
from webassets import Environment, Bundle
from webassets.script import CommandLineEnvironment
from pytsite.core import reg as _reg, logger as _logger, console as _console
from . import _functions


class BuildAssets(_console.command.Abstract):
    """assetman:build Console Command.
    """
    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'assetman:build'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.core.lang import t
        return t('pytsite.core@assetman_console_command_description')

    def execute(self, **kwargs: dict):
        """Execute The Command.
        """
        static_dir = _reg.get('paths.static')
        debug = _reg.get('debug.enabled')

        if _path.exists(static_dir):
            rmtree(static_dir)

        for pkg_name, package_assets_dir in _functions.get_packages().items():
            # Building package's assets absolute paths list
            files_list = []
            for root, dirs, files in _walk(package_assets_dir):
                for file in files:
                    files_list.append(_path.join(root, file))

            for src in files_list:
                if '.webassets-cache' in src:
                    continue

                dst = src.replace(package_assets_dir + _path.sep, '')
                dst = _path.join(static_dir, 'assets', pkg_name, dst)

                ext = _path.splitext(src)[1]
                if ext in ['.js', '.css', '.less']:
                    filters = []

                    if ext == '.less':
                        filters.append('less')
                        dst = re.sub(r'\.less$', '.css', dst)
                        ext = '.css'

                    if ext == '.js' and _reg.get('output.minify') and not src.endswith('.min.js'):
                        filters.append('rjsmin')

                    if ext == '.css' and _reg.get('output.minify') and not src.endswith('.min.css'):
                        filters.append('cssutils')

                    bundle = Bundle(src, filters=filters)
                    env = Environment(directory=package_assets_dir, debug=debug, versions=False,
                                      manifest=False, cache=False)
                    env.register('bundle', bundle, output=dst)

                    _console.print_info('Compiling {} -> {}'.format(src, dst))
                    cmd = CommandLineEnvironment(env, _logger)
                    cmd.invoke('build', {})
                elif '.webassets-cache' not in src:
                    dst_dir = _path.dirname(dst)
                    if not _path.exists(dst_dir):
                        _makedirs(dst_dir, 0o755)
                    copy(src, dst)

        _console.run_command('lang:build')
