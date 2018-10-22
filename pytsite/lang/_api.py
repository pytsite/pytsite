"""PytSite Localization API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import yaml as _yaml
import re as _re
from typing import List as _List, Callable as _Callable, Dict as _Dict
from importlib.util import find_spec as _find_spec
from datetime import datetime as _datetime
from os import path as _path
from pytsite import threading as _threading, events as _events
from . import _error

_languages = []
_current = {}  # Thread safe current language
_default = None  # type: str
_packages = {}
_globals = {}
_translated_strings_cache = {}

_SUB_TRANS_TOKEN_RE = _re.compile('{:([_a-z0-9@]+)}')

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
    """Define available languages
    """
    global _languages
    _languages = languages

    set_current(_languages[0])
    set_fallback(_languages[0])


def is_defined(language: str):
    """Check whether a language is defined.
    """
    return language in _languages


def langs(include_current: bool = True) -> _List[str]:
    """Get all defined languages
    """
    r = _languages.copy()

    if not include_current:
        r.remove(_current[_threading.get_id()])

    return r


def set_current(language: str):
    """Set current language
    """
    if language not in _languages:
        raise _error.LanguageNotSupported("Language '{}' is not supported".format(language))

    _current[_threading.get_id()] = language


def set_fallback(language: str):
    """Set fallback language
    """
    if language not in _languages:
        raise _error.LanguageNotSupported("Language '{}' is not supported".format(language))

    global _default
    _fallback = language


def get_current() -> str:
    """Get current language
    """
    if not _languages:
        raise RuntimeError('No languages are defined')

    tid = _threading.get_id()
    if tid not in _current:
        _current[_threading.get_id()] = _languages[0]

    return _current[_threading.get_id()]


def get_primary() -> str:
    """Get primary language
    """
    if not _languages:
        raise RuntimeError('There are no languages defined')

    return _languages[0]


def get_fallback() -> str:
    """Get fallback language
    """
    if not _languages:
        raise RuntimeError('No languages are defined')

    return _default


def is_package_registered(pkg_name):
    """Check if the package already registered
    """
    return pkg_name in _packages


def register_package(pkg_name: str, languages_dir: str = 'res/lang'):
    """Register language container
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


def register_global(name: str, handler: _Callable):
    """Register a global
    """
    if name in _globals:
        raise RuntimeError("Language global '{}' is already registered".format(name))

    if not callable(handler):
        raise TypeError("{} is not callable".format(type(handler)))

    _globals[name] = handler


def get_packages() -> dict:
    """Get info about registered packages
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


def t(msg_id: str, args: dict = None, language: str = None, exceptions: bool = False, use_fallback: bool = True) -> str:
    """Translate a message
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

    # Try to get message translation string from cache
    cache_key = '{}-{}@{}'.format(language, package_name, msg_id)
    msg = _translated_strings_cache.get(cache_key)

    # Message translation is not found in cache, try to fetch it
    if not msg:
        # Try to get translation via event
        for r in _events.fire('pytsite.lang@translate', language=language, package_name=package_name, msg_id=msg_id):
            msg = r

        # Load translation from package's data
        if not msg:
            lang_file_content = get_package_translations(package_name, language)

            if msg_id not in lang_file_content:
                # Searching for fallback translation
                fallback = get_fallback()
                if use_fallback and fallback != language:
                    return t(package_name + '@' + msg_id, args, fallback, exceptions, False)
                else:
                    if exceptions:
                        raise _error.TranslationError(
                            "Translation is not found for '{}@{}'".format(package_name, msg_id))
                    else:
                        return package_name + '@' + msg_id

            msg = lang_file_content[msg_id]

        # Cache translation string
        _translated_strings_cache[cache_key] = msg

    # Replace placeholders
    if args:
        for k, v in args.items():
            msg = msg.replace(':' + str(k), str(v))

    # Replace sub-translations
    msg = _SUB_TRANS_TOKEN_RE.sub(lambda match: t(match.group(1)), msg)

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


def get_package_translations(pkg_name: str, language: str = None) -> _Dict[str, str]:
    """Load package's language file
    """
    # Is the package registered?
    if not is_package_registered(pkg_name):
        plugins_pkg_name = 'plugins.' + pkg_name
        if is_package_registered(plugins_pkg_name):
            pkg_name = plugins_pkg_name
        else:
            raise _error.PackageNotRegistered("Language package '{}' is not registered".format(pkg_name))

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


def pretty_date(date_time: _datetime) -> str:
    """Format date as pretty string.
    """
    r = '{} {}'.format(date_time.day, t_plural('pytsite.lang@month_' + str(date_time.month)))

    if date_time.now().year != date_time.year:
        r += ' ' + str(date_time.year)

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


def on_translate(handler, priority: int = 0):
    """Shortcut
    """
    _events.listen('pytsite.lang@translate', handler, priority)


def on_split_msg_id(handler, priority: int = 0):
    """Shortcut
    """
    _events.listen('pytsite.lang@split_msg_id', handler, priority)


def clear_cache():
    """Clear translations cache
    """
    global _translated_strings_cache

    _translated_strings_cache = {}


def _split_msg_id(msg_id: str) -> list:
    """Split message ID into message ID and package name.
    """
    for r in _events.fire('pytsite.lang@split_msg_id', msg_id=msg_id):
        msg_id = r

    return msg_id.split('@')[:2] if '@' in msg_id else ['app', msg_id]
