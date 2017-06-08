"""PytSite Language Support
"""
import yaml as _yaml
import re as _re
import json as _json
from typing import List as _List, Callable as _Callable
from importlib.util import find_spec as _find_spec
from datetime import datetime as _datetime
from os import path as _path, makedirs as _makedirs
from pytsite import lang as _lang, logger as _logger, theme as _theme, threading as _threading
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_languages = []
_current = {}  # Thread safe current language
_fallback = None  # type: str
_packages = {}
_globals = {}
_sub_trans_token_re = _re.compile('{:([_a-z0-9@]+)}')

_default_regions = {
    'en': 'US',
    'ru': 'RU',
    'uk': 'UA',
}


def _global_re_handler(match: _re) -> str:
    f_name = match.group(1)
    if f_name not in _globals:
        return match.group(0)

    try:
        return _globals[f_name]()
    except Exception as e:
        raise RuntimeError('Error while calling lang function {}(): {}'.format(f_name, e))


def define(languages: list):
    """Define available languages.
    """
    global _languages
    _languages = languages

    # Append 'neutral' language
    languages.append('n')

    set_current(_languages[0])
    set_fallback(_languages[0])


def is_defined(language: str):
    """Check whether a language is defined.
    """
    return language in _languages


def langs(include_current: bool = True, include_neutral: bool = False) -> _List[str]:
    """Get all available languages.
    """
    r = _languages.copy()

    if not include_neutral:
        r.remove('n')

    if not include_current:
        r.remove(_current[_threading.get_id()])

    return r


def set_current(language: str):
    """Set current default language.
    """
    if language not in _languages:
        raise _error.LanguageNotSupported("Language '{}' is not supported".format(language))

    _current[_threading.get_id()] = language


def set_fallback(language: str):
    """Set fallback language.
    """
    if language not in _languages:
        raise _error.LanguageNotSupported("Language '{}' is not supported".format(language))

    global _fallback
    _fallback = language


def get_current() -> str:
    """Get current language.
    """
    if not _languages:
        raise RuntimeError("No languages are defined")

    tid = _threading.get_id()
    if tid not in _current:
        _current[_threading.get_id()] = _languages[0]

    return _current[_threading.get_id()]


def get_primary() -> str:
    """Get primary language.
    """
    if not _languages:
        raise RuntimeError("No languages are defined")

    return _languages[0]


def get_fallback() -> str:
    """Get fallback language.
    """
    if not _languages:
        raise RuntimeError("No languages are defined")

    return _fallback


def is_package_registered(pkg_name):
    """Check if the package already registered.
    """
    return pkg_name in _packages


def register_package(pkg_name: str, languages_dir: str = 'res/lang', alias: str = None):
    """Register language container.
    """
    spec = _find_spec(pkg_name)
    if not spec or not spec.loader:
        raise RuntimeError("Package '{}' is not found".format(pkg_name))

    lng_dir = _path.join(_path.dirname(spec.origin), languages_dir)
    if not _path.isdir(lng_dir):
        raise RuntimeError("Language directory '{}' is not found".format(lng_dir))

    if pkg_name in _packages:
        raise _error.PackageAlreadyRegistered("Language package '{}' already registered".format(pkg_name))
    _packages[pkg_name] = {'__path': lng_dir}

    if alias:
        if alias in _packages:
            raise RuntimeError("Package alias '{}' already registered".format(alias))
        _packages[alias] = {'__path': lng_dir}


def register_global(name: str, handler: _Callable):
    """Register a global.
    """
    if name in _globals:
        raise RuntimeError("Function '{}' is already registered".format(name))

    if not callable(handler):
        raise TypeError("{} is not callable".format(type(handler)))

    _globals[name] = handler


def get_packages() -> dict:
    """Get info about registered packages.
    """
    return _packages


def is_translation_defined(msg_id: str, language: str = None, use_fallback=True) -> bool:
    """Check if the translation is defined for message ID.
    """
    try:
        t(msg_id, None, language, True, use_fallback)
        return True
    except (_error.TranslationError, _error.PackageNotRegistered):
        return False


def t(msg_id: str, args: dict = None, language: str = None, exceptions=False, use_fallback=True) -> str:
    """Translate a message ID.
    """
    global _globals

    if not language:
        language = get_current()

    if language not in _languages:
        raise _error.LanguageNotSupported("Language '{}' is not supported".format(language))

    if msg_id in _globals:
        return _globals[msg_id](language, args)

    # Determining package name and message ID
    package_name, msg_id = _split_msg_id(msg_id)

    # Loading language file data
    lang_file_content = load_lang_file(package_name, language)

    if msg_id not in lang_file_content:
        # Searching for fallback translation
        fallback = get_fallback()
        if use_fallback and fallback != language:
            return t(package_name + '@' + msg_id, args, fallback, exceptions, False)
        else:
            if exceptions:
                raise _error.TranslationError("Translation is not found for '{}@{}'".format(package_name, msg_id))
            else:
                return package_name + '@' + msg_id

    msg = lang_file_content[msg_id]

    # Replacing placeholders
    if args:
        for k, v in args.items():
            msg = msg.replace(':' + str(k), str(v))

    # Replacing sub-translations
    msg = _sub_trans_token_re.sub(lambda match: t(match.group(1)), msg)

    return msg


def t_plural(msg_id: str, num: int = 2, language: str = None) -> str:
    """Translate a string in plural form.
    """
    if not language:
        language = get_current()

    if language in ['en']:
        if num == 1:
            return t(msg_id + '_plural_one')
        else:
            return t(msg_id + '_plural_two')

    # Language is not english
    if 11 <= num <= 19:
        return t(msg_id + '_plural_zero')
    else:
        last_digit = int(str(num)[-1])
        if last_digit in [0, 5, 6, 7, 8, 9]:
            return t(msg_id + '_plural_zero')
        elif last_digit in [2, 3, 4]:
            return t(msg_id + '_plural_two')
        else:
            return t(msg_id + '_plural_one')


def lang_title(language: str = None) -> str:
    """Get human readable language name.
    """
    if not language:
        language = get_current()

    try:
        return t('pytsite.lang@lang_title_' + language, exceptions=True)
    except _error.TranslationError:
        try:
            return t('app@lang_title_' + language, exceptions=True)
        except _error.TranslationError:
            return language


def load_lang_file(pkg_name: str, language: str = None):
    """Load package's language file.

    :rtype: dict[str, str]
    """
    # Is the package registered?
    if not is_package_registered(pkg_name):
        raise _error.PackageNotRegistered("Package '{}' is not registered".format(pkg_name))

    if not language:
        language = get_current()

    # Getting from cache
    if language in _packages[pkg_name]:
        return _packages[pkg_name][language]

    content = {}

    # Actual data loading
    file_path = _path.join(_packages[pkg_name]['__path'], language + '.yml')
    if not _path.exists(file_path):
        return content

    with open(file_path, encoding='utf-8') as f:
        content = _yaml.load(f)

    if content is None:
        content = {}

    # Caching
    _packages[pkg_name][language] = content

    return content


def time_ago(time: _datetime) -> str:
    """Format date/time as 'time ago' phrase.
    """
    diff = _datetime.now() - time
    """:type: datetime.timedelta"""

    if diff.days:
        if diff.days > 365:
            years = diff.days // 365
            return '{} {}'.format(years, t_plural('pytsite.lang@year', years))
        elif diff.days > 31:
            months = diff.days // 12
            return '{} {}'.format(months, t_plural('pytsite.lang@month', months))
        elif diff.days > 7:
            weeks = diff.days // 7
            return '{} {}'.format(weeks, t_plural('pytsite.lang@week', weeks))
        else:
            return '{} {}'.format(diff.days, t_plural('pytsite.lang@day', diff.days))
    else:
        if diff.seconds > 3600:
            hours = diff.seconds // 3600
            return '{} {}'.format(hours, t_plural('pytsite.lang@hour', hours))
        elif diff.seconds > 60:
            minutes = diff.seconds // 60
            return '{} {}'.format(minutes, t_plural('pytsite.lang@minute', minutes))
        else:
            if diff.seconds:
                return '{} {}'.format(diff.seconds, t_plural('pytsite.lang@second', diff.seconds))
            else:
                return t('pytsite.lang@just_now')


def pretty_date(time: _datetime) -> str:
    """Format date as pretty string.
    """
    r = '{} {}'.format(time.day, t_plural('pytsite.lang@month_' + str(time.month)))

    diff = _datetime.now() - time
    if abs(diff.days) > 365:
        r += ' ' + str(time.year)

    return r


def pretty_date_time(time: _datetime) -> str:
    """Format date/time as pretty string.
    """
    return '{}, {}'.format(pretty_date(time), time.strftime('%H:%M'))


def ietf_tag(language: str = None, region: str = None, sep: str = '-') -> str:
    global _default_regions

    if not language:
        language = get_current()

    if not region:
        region = _default_regions[language] if language in _default_regions else language

    return language.lower() + sep + region.upper()


def build():
    """Compile translations.
    """
    from pytsite import assetman, console, tpl

    console.print_info(_lang.t('pytsite.assetman@compiling_translations'))

    translations = {}
    for lang_code in _lang.langs():
        translations[lang_code] = {}
        for pkg_name, info in _lang.get_packages().items():
            _logger.info('Compiling translations for {} ({})'.format(pkg_name, lang_code))
            translations[lang_code][pkg_name] = _lang.load_lang_file(pkg_name, lang_code)

    # Write translations to static file
    output_file = _path.join(assetman.get_dst_dir_path('pytsite.lang'), 'translations.js')
    output_dir = _path.dirname(output_file)

    if not _path.exists(output_dir):
        _makedirs(output_dir, 0o755, True)

    with open(output_file, 'wt', encoding='utf-8') as f:
        _logger.info("Writing translations into '{}'".format(output_file))
        f.write(tpl.render('pytsite.lang@translations-js', {
            'langs_json': _json.dumps(_lang.langs()),
            'translations_json': _json.dumps(translations),
        }))


def _split_msg_id(msg_id: str) -> list:
    """Split message ID into message ID and package name.
    """
    if '@' not in msg_id:
        msg_id = '$theme@' + msg_id

    if '$theme' in msg_id:
        msg_id = msg_id.replace('$theme', _theme.get().name)

    return msg_id.split('@')[:2]
