"""PytSite Language Support
"""
import yaml as _yaml
from importlib.util import find_spec as _find_spec
from datetime import datetime as _datetime
from os import path as _path
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__languages = []
__current_language = None
__packages = {}


def define(languages: list):
    """Define available languages.
    """
    global __languages
    __languages = languages
    set_current(languages[0])


def langs():
    """Get all available languages.
    """
    return __languages


def set_current(code: str):
    """Set current default language.
    """
    if code not in __languages:
        raise _error.LanguageNotSupported("Language '{}' is not supported.".format(code))

    global __current_language
    __current_language = code


def get_current() -> str:
    """Get current language.
    """
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


def register_package(pkg_name: str, languages_dir: str='res/lang') -> str:
    """Register language container.
    """
    if is_package_registered(pkg_name):
        return

    spec = _find_spec(pkg_name)
    if not spec or not spec.loader:
        raise Exception("Package '{}' is not found.".format(pkg_name))

    lng_dir = _path.join(_path.dirname(spec.origin), languages_dir)
    if not _path.isdir(lng_dir):
        raise Exception("Directory '{}' is not exists.".format(lng_dir))

    __packages[pkg_name] = {'__path': lng_dir}


def get_packages() -> dict:
    return __packages


def t(msg_id: str, args: dict=None, language: str=None) -> str:
    """Translate a string.
    """
    if not language:
        language = get_current()

    if language not in __languages:
        raise _error.TranslationError("Language '{}' is not supported.".format(language))

    # Determining package name and message ID
    package_name = 'app'
    msg_id = msg_id.split('@')
    if len(msg_id) == 2:
        package_name = msg_id[0]
        msg_id = msg_id[1]
    else:
        msg_id = msg_id[0]

    content = load_lang_file(package_name, language)
    if msg_id not in content:
        raise _error.TranslationError("Translation is not found for '{}'".format(package_name + '@' + msg_id))

    msg = content[msg_id]
    """:type : str"""

    if args:
        for k, v in args.items():
            msg = msg.replace(':' + str(k), str(v))

    return msg


def t_plural(msg_id: str, num: int=2, language: str=None) -> str:
    """Translate a string in plural form.
    """
    if not language:
        language = get_current()

    # Language is not cyrillic
    if language not in ['ru', 'uk']:
        if num == 1:
            return t(msg_id + '_plural_one')
        else:
            return t(msg_id + '_plural_two')

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


def lang_title(language: str=None) -> str:
    """Get human readable language name.
    """
    if not language:
        language = get_current()
    try:
        return t('lang_title_' + language)
    except _error.TranslationError:
        return language


def load_lang_file(package_name: str, language: str=None):
    """Load package's language file.
    """
    # Is the package registered?
    if package_name not in __packages:
        raise Exception("Package '{}' is not registered.".format(package_name))

    if not language:
        language = get_current()

    # Getting from cache
    if language in __packages[package_name]:
        return __packages[package_name][language]

    content = {}

    # Actual data loading
    file_path = _path.join(__packages[package_name]['__path'], language + '.yml')
    if not _path.exists(file_path):
        return content

    with open(file_path) as f:
        content = _yaml.load(f)

    if content is None:
        content = {}

    # Caching
    __packages[package_name][language] = content

    return content


def time_ago(time: _datetime) -> str:
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
            return '{} {}'.format(diff.seconds, t_plural('pytsite.lang@second', diff.seconds))


def pretty_date(time: _datetime) -> str:
    r = '{} {}'.format(time.day, t_plural('pytsite.lang@month_' + str(time.month)))

    diff = _datetime.now() - time
    if diff.days > 365:
        r += ' ' + str(time.year)

    return r


def pretty_date_time(time: _datetime) -> str:
    return '{}, {}'.format(pretty_date(time), time.strftime('%H:%M'))
