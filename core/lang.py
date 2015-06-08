"""PytSite Language Support.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import yaml
import json
from importlib.util import find_spec
from os import path
from . import console, reg


class TranslationError(Exception):
    pass


class ConsoleCommand(console.AbstractCommand):
    def get_name(self)->str:
        return 'lang:build'

    def get_description(self)->str:
        return t('pytsite.core@lang_console_command_description')

    def execute(self, **kwargs: dict):
        compile_translations()

__languages = []
__current_language = None
__packages = {}


def define_languages(languages: list):
    """Define available languages.
    """

    global __languages
    __languages = languages
    set_current_lang(languages[0])


def get_langs():
    """Get all available languages.
    """
    return __languages


def set_current_lang(code: str):
    """Set current default language.
    """
    if code not in __languages:
        raise Exception("Language '{0}' is not defined.".format(code))

    global __current_language
    __current_language = code


def get_current_lang()->str:
    """Get current language.
    """
    global __languages
    if not __languages:
        raise Exception("No languages are defined.")

    global __current_language
    if not __current_language:
        __current_language = __languages[0]

    return __current_language


def is_package_registered(pkg_name):
    """Check if the package already registered.
    """
    return pkg_name in __packages


def register_package(pkg_name: str, languages_dir: str='lang') -> str:
    """Register language container.
    """
    if is_package_registered(pkg_name):
        raise Exception("Package '{}' is already registered.")

    spec = find_spec(pkg_name)
    if not spec:
        raise Exception("Package '{}' is not found.".format(pkg_name))

    lng_dir = path.join(path.dirname(spec.origin), languages_dir)
    if not path.isdir(lng_dir):
        raise Exception("Directory '{}' is not exists.".format(lng_dir))

    __packages[pkg_name] = {'__path': lng_dir}


def t(msg_id: str, data: dict=None, language: str=None)->str:
    """Translate a string.
    """
    if not language:
        language = get_current_lang()

    if language not in __languages:
        raise TranslationError("Language '{}' is not defined.".format(language))

    # Determining package name and message ID
    package_name = 'app'
    msg_id = msg_id.split('@')
    if len(msg_id) == 2:
        package_name = msg_id[0]
        msg_id = msg_id[1]
    else:
        msg_id = msg_id[0]

    content = _load_file(package_name, language)
    if msg_id not in content:
        raise TranslationError("Translation is not found for '{}'".format(package_name + '@' + msg_id))

    msg = content[msg_id]
    """:type : str"""

    if data:
        for k, v in data.items():
            msg = msg.replace(':' + str(k), str(v))

    return msg


def t_plural(msg_id: str, num: int=2, language: str=None)->str:
    """Translate a string in plural form.
    """
    if not language:
        language = get_current_lang()

    # Language is not cyrillic
    if language not in ['ru', 'uk']:
        if num == 1:
            return t(msg_id + '_plural_one')
        else:
            return t(msg_id + '_plural_two')

    last_digit = int(str(num)[-1])
    if last_digit in [0, 5, 6, 7, 8, 9]:
        return t(msg_id + '_plural_zero')
    elif last_digit in [2, 3, 4]:
        return t(msg_id + '_plural_two')
    else:
        return t(msg_id + '_plural_one')


def get_lang_title(code: str) -> str:
    """Get human readable language name.
    """
    return t('lang_title_' + code)


def compile_translations(print_output: bool=True):
    """Compile language translations.
    """

    translations = {}
    for lang_code in get_langs():
        translations[lang_code] = {}
        for pkg_name, info in __packages.items():
            if print_output:
                print("Compiling translations for {} ({})".format(pkg_name, lang_code))
            translations[lang_code][pkg_name] = _load_file(pkg_name, lang_code)

    str_output = 'pytsite.lang.langs={};'.format(json.dumps(get_langs()))
    str_output += 'pytsite.lang.current_lang="{}";'.format(get_current_lang())
    str_output += 'pytsite.lang.translations={};'.format(json.dumps(translations))
    output_file = path.join(reg.get('paths.static'), 'assets', 'app', 'js', 'translations.js')
    with open(output_file, 'wt') as f:
        if print_output:
            print("Writing translations into '{}'".format(output_file))
        f.write(str_output)


def _load_file(package_name: str, language: str=None):
    """Load package's language file.
    """

    # Is the package registered?
    if package_name not in __packages:
        raise Exception("Package '{0}' is not registered.".format(package_name))

    if not language:
        language = get_current_lang()

    # Getting from cache
    if language in __packages[package_name]:
        return __packages[package_name][language]

    content = {}

    # Actual data loading
    file_path = path.join(__packages[package_name]['__path'], language + '.yml')
    if not path.exists(file_path):
        return content

    with open(file_path) as f:
        content = yaml.load(f)

    if content is None:
        content = {}

    # Caching
    __packages[package_name][language] = content

    return content
