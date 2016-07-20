"""Assetman Console Commands.
"""
import re as _re
import json as _json
from os import path as _path, walk as _walk, makedirs as _makedirs
from shutil import rmtree as _rmtree, copy as _copy
from webassets import Environment as _Environment, Bundle as _Bundle
from webassets.script import CommandLineEnvironment as _CommandLineEnvironment
from pytsite import reg as _reg, console as _console, logger as _logger, lang as _lang, validation as _validation, \
    maintenance as _maintenance, events as _events
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Assetman(_console.command.Abstract):
    """assetman:build Console Command.
    """

    def get_name(self) -> str:
        """Get name of the command.
        """
        return 'assetman'

    def get_description(self) -> str:
        """Get description of the command.
        """
        from pytsite.lang import t
        return t('pytsite.assetman@assetman_console_command_description')

    def get_options_help(self) -> str:
        """Get help for the command.
        """
        return '--build [--no-maintenance]'

    def get_options(self) -> tuple:
        """Get command options.
        """
        return (
            ('build', _validation.rule.Pass()),
            ('no-maintenance', _validation.rule.Pass()),
        )

    def _build(self, maintenance=True):
        static_dir = _reg.get('paths.static')
        assets_dir = _path.join(static_dir, 'assets')
        if _path.exists(assets_dir):
            _rmtree(assets_dir)

        if maintenance:
            _maintenance.enable()

        _console.print_info(_lang.t('pytsite.assetman@compiling_assets'))
        for pkg_name, package_assets_dir in _api.get_packages().items():
            # Building package's assets absolute paths list
            files_list = []
            for root, dirs, files in _walk(package_assets_dir):
                for file in files:
                    files_list.append(_path.join(root, file))

            for src in files_list:
                if '.webassets-cache' in src:
                    continue

                dst = src.replace(package_assets_dir + _path.sep, '')
                dst = _path.join(assets_dir, pkg_name, dst)

                ext = _path.splitext(src)[1]
                if ext in ['.js', '.css', '.ts', '.less']:
                    filters = []
                    env = _Environment(directory=package_assets_dir, debug=_reg.get('debug', False), versions=False,
                                       manifest=False, cache=False)

                    # LESS compiler
                    if ext == '.less':
                        filters.append('less')
                        dst = _re.sub(r'\.less$', '.css', dst)
                        ext = '.css'

                    # TypeScript compiler
                    elif ext == '.ts':
                        filters.append('typescript')
                        dst = _re.sub(r'\.ts$', '.js', dst)
                        ext = '.js'

                    # Minifying JS/CSS
                    if _reg.get('output.minify'):
                        if ext == '.js' and not src.endswith('.min.js') and not src.endswith('.pack.js'):
                            filters.append('jsmin')
                        if ext == '.css' and not src.endswith('.min.css'):
                            filters.append('cssmin')

                    bundle = _Bundle(src, filters=filters)
                    env.register('bundle', bundle, output=dst)

                    _logger.info('Compiling {} -> {}'.format(src, dst))
                    cmd = _CommandLineEnvironment(env, _logger)
                    cmd.invoke('build', {})

                # Just copy file as is
                elif '.webassets-cache' not in src:
                    dst_dir = _path.dirname(dst)
                    if not _path.exists(dst_dir):
                        _makedirs(dst_dir, 0o755)
                    _copy(src, dst)

        # Compile translations
        _console.print_info(_lang.t('pytsite.assetman@compiling_translations'))
        translations = {}
        for lang_code in _lang.langs():
            translations[lang_code] = {}
            for pkg_name, info in _lang.get_packages().items():
                _logger.info("Compiling translations for {} ({})".format(pkg_name, lang_code))
                translations[lang_code][pkg_name] = _lang.load_lang_file(pkg_name, lang_code)

        str_output = 'pytsite.lang.langs={};'.format(_json.dumps(_lang.langs()))
        str_output += 'pytsite.lang.translations={};'.format(_json.dumps(translations))
        output_file = _path.join(_reg.get('paths.static'), 'assets', 'app', 'js', 'translations.js')
        output_dir = _path.dirname(output_file)
        if not _path.exists(output_dir):
            _makedirs(output_dir, 0o755, True)
        with open(output_file, 'wt', encoding='utf-8') as f:
            _logger.info("Writing translations into '{}'".format(output_file))
            f.write(str_output)

        _events.fire('pytsite.assetman.build.after')

        if maintenance:
            _maintenance.disable()

    def execute(self, args: tuple = (), **kwargs):
        """Execute The Command.
        """
        if not kwargs:
            return _console.run_command('help', ('assetman',))

        if 'build' in kwargs:
            self._build(not kwargs.get('no-maintenance', False))
