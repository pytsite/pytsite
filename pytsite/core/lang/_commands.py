"""Lang Plugin Console Commands.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import json
from os import path as _path, makedirs as _makedirs
from pytsite.core import reg as _reg, console as _console
from . import _functions

class CompileTranslations(_console.command.Abstract):
    """Compile Translations Console Command.
    """

    def get_name(self) -> str:
        return 'lang:build'

    def get_description(self) -> str:
        return _functions.t('core@lang_console_command_description')

    def execute(self, **kwargs: dict):
        """Compile language translations.
        """
        translations = {}
        for lang_code in _functions.get_langs():
            translations[lang_code] = {}
            for pkg_name, info in _functions.get_packages().items():
                _console.print_info("Compiling translations for {} ({})".format(pkg_name, lang_code))
                translations[lang_code][pkg_name] = _functions.load_lang_file(pkg_name, lang_code)

        str_output = 'pytsite.lang.langs={};'.format(json.dumps(_functions.get_langs()))
        str_output += 'pytsite.lang.current_lang="{}";'.format(_functions.get_current_lang())
        str_output += 'pytsite.lang.translations={};'.format(json.dumps(translations))
        output_file = _path.join(_reg.get('paths.static'), 'assets', 'app', 'js', 'translations.js')
        output_dir = _path.dirname(output_file)
        if not _path.exists(output_dir):
            _makedirs(output_dir, 0o755, True)
        with open(output_file, 'wt') as f:
            _console.print_info("Writing translations into '{}'".format(output_file))
            f.write(str_output)
