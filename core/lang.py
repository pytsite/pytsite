"""PytSite Language Support.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from importlib.util import find_spec
from os import path
import yaml

__languages = []
__current_language = None
__packages = {}


def define_languages(languages: list):
    """Define available languages.
    """
    global __languages
    __languages = languages
    set_current_lang(languages[0])


def get_languages():
    """Get all available languages.
    """
    return __languages


def set_current_lang(code: str):
    """Set current default language.
    """
    if code not in __languages:
        raise Exception("Language '{0}' is not defined.".format(code))


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


def register_package(package_name: str, languages_dir: str='lang')->str:
    """Register language container.
    """
    spec = find_spec(package_name)
    if not spec:
        raise Exception("Package '{0}' is not found.".format(package_name))

    lng_dir = path.join(path.dirname(spec.origin), languages_dir)
    if not path.isdir(lng_dir):
        raise Exception("Directory '{0}' is not exists.".format(lng_dir))

    __packages[package_name] = {'_path': lng_dir}


def t(msg_id: str, data: dict=None, language: str=None)->str:
    """Translate a string.
    """
    if not language:
        language = get_current_lang()

    if language not in __languages:
        raise Exception("Language '{0}' is not defined.".format(language))

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
        return package_name + '@' + msg_id

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


def transliterate(text: str)->str:
    """Transliterate a string.
    """
    cyrillic = [
        "Щ", "щ", 'Ё', 'Ж', 'Х', 'Ц', 'Ч', 'Ш', 'Ю', 'Я',
        'ё', 'ж', 'х', 'ц', 'ч', 'ш', 'ю', 'я', 'А', 'Б',
        'В', 'Г', 'Д', 'Е', 'З', 'И', 'Й', 'К', 'Л', 'М',
        'Н', 'О', 'П', 'Р', 'С', 'Т', 'У', 'Ф', 'Ь', 'Ы',
        'Ъ', 'Э', 'а', 'б', 'в', 'г', 'д', 'е', 'з', 'и',
        'і', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с',
        'т', 'у', 'ф', 'ь', 'ы', 'ъ', 'э', 'Ї', 'ї', 'Є',
        'є', 'Ґ', 'ґ']

    roman = [
        "Sch", "sch", 'Yo', 'Zh', 'Kh', 'Ts', 'Ch', 'Sh', 'Yu', 'Ya',
        'yo', 'zh', 'kh', 'ts', 'ch', 'sh', 'yu', 'ya', 'A', 'B',
        'V', 'G', 'D', 'E', 'Z', 'I', 'Y', 'K', 'L', 'M',
        'N', 'O', 'P', 'R', 'S', 'T', 'U', 'F', '', 'Y',
        '', 'E', 'a', 'b', 'v', 'g', 'd', 'e', 'z', 'i',
        'i', 'y', 'k', 'l', 'm', 'n', 'o', 'p', 'r', 's',
        't', 'u', 'f', '', 'y', '', 'e', 'i', 'i', 'Ye',
        'ye', 'G', 'g'
    ]

    r = ''
    for ch in text:
        try:
            i = cyrillic.index(ch)
            r += roman[i]
        except ValueError:
            r += ch

    return r


def _load_file(package_name: str, language: str=None):
    """Load package's language file.
    """
    # Is package registered?
    if package_name not in __packages:
        raise Exception("Package '{0}' is not registered.".format(package_name))

    if not language:
        language = get_current_lang()

    # Getting from cache
    if language in __packages[package_name]:
        return __packages[package_name][language]

    # Actual data loading

    file_path = path.join(__packages[package_name]['_path'], language + '.yml')
    file = open(file_path)
    content = yaml.load(file)
    file.close()

    if content is None:
        content = dict()

    # Caching
    __packages[package_name][language] = content

    return content
