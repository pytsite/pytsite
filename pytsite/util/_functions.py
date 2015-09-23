"""PytSite Helper Functions.
"""
import random as _random, re as _re
from copy import deepcopy as _deepcopy
from werkzeug.utils import escape as _escape_html


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def escape_html(s: str) -> str:
    """Escape an HTML string.
    """
    return _escape_html(s)


def dict_merge(a: dict, b: dict) -> dict:
    """Recursively merge dicts.

    Not just simple a['key'] = b['key'], if both a and b have a key who's
    value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.
    https://www.xormedia.com/recursively-merge-dictionaries-in-python/"""

    if not isinstance(a, dict) or not isinstance(b, dict):
        raise ValueError('Expected both dictionaries as arguments.')

    result = _deepcopy(a)

    for k, v in b.items():
        if k in result and isinstance(result[k], dict):
                result[k] = dict_merge(result[k], v)
        else:
            result[k] = _deepcopy(v)

    return result


def mk_tmp_file() -> tuple:
    """Create temporary file.
    """
    from os import path, mkdir
    from tempfile import mkstemp
    from pytsite import reg

    tmp_dir = reg.get('paths.tmp')
    if not tmp_dir:
        raise Exception("Cannot determine temporary directory location.")

    if not path.exists(tmp_dir):
        mkdir(tmp_dir)

    return mkstemp(dir=tmp_dir)


def random_str(size=16, chars='0123456789abcdef'):
    """Generate random string.
    """
    return ''.join(_random.choice(chars) for _ in range(size))


def random_password(size=16):
    """Generate random password.
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-`~|\/.,?><{}[]":;'
    return random_str(size, chars)


def weight_sort(inp: list, key: str='weight') -> list:
    """Sort list by weight.
    """
    return sorted(inp, key=lambda x: x[key])


def html_attrs_str(attrs: dict, replace_keys: dict=None) -> str:
    """Format dictionary as XML attributes string.
    """
    single_attrs = 'checked', 'selected', 'required', 'allowfullscreen', 'hidden'

    r = ''
    for k, v in attrs.items():
        k = k.strip()
        if replace_keys and k in replace_keys:
            k = replace_keys[k]

        if v is not None:
            if k in single_attrs:
                if v:
                    r += ' {}'.format(k)
            else:
                v = str(v).strip()
                r += ' {}="{}"'.format(k, _escape_html(v))

    return r


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


def transform_str_1(s: str) -> str:
    """Transform a string, variant 1.
    """
    mapping = {
        '!': '', '@': '', '#': '', '$': '', '%': '', '^': '', '&': '', '*': '', '(': '', ')': '', '_': '',
        '=': '', '+': '', '"': '', "'": '', '{': '', '}': '', '[': '', ']': '', '`': '', '~': '', '|': '', '\\': '',
        '?': '', '.': '', ',': '', '<': '', '>': '', '«': '', '»': '', '№': '', ':': '', ';': '',
    }

    for k, v in mapping.items():
        s = s.replace(k, v)

    s = transliterate(s.lower())
    s = _re.sub('/{2,}', '/', s)
    s = _re.sub('[^a-zA-Z0-9/]', '-', s)
    s = _re.sub('-{2,}', '-', s)
    s = _re.sub('(^-|-$)', '', s)

    return s


def transform_str_2(s: str) -> str:
    """Transform a string, variant 2.
    """
    return _re.sub('/', '-', transform_str_1(s))


def get_class(s: str) -> type:
    """Get class by its fully qualified name.
    """
    class_fqn = list_cleanup(s.split('.'))
    if len(class_fqn) < 2:
        raise Exception("Cannot determine class name from string '{}'.".format(s))

    class_name = class_fqn[-1:][0]
    module_name = '.'.join(class_fqn[:-1])
    module = __import__(module_name, fromlist=[class_name])

    return getattr(module, class_name)


def list_cleanup(inp: list) -> list:
    """Remove empty values from list.
    """
    r = []
    for v in inp:
        if isinstance(v, str):
            v = v.strip()
        if v:
            r.append(v)

    return r


def dict_cleanup(inp: dict) -> dict:
    """Remove empty values from dict.
    """
    r = {}
    for k, v in inp.items():
        if isinstance(v, str):
            v = v.strip()
        if v:
            r[k] = v

    return r


def nav_link(href: str, anchor: str, **kwargs: dict) -> str:
    """Generate 'navigation' link.
    """
    from pytsite import html, router

    if not href:
        raise ValueError('href cannot be empty.')

    li = html.Li()
    if href != '#' and router.url(href, strip_query=True) == router.current_url(strip_query=True):
        li.set_attr('cls', 'active')

    return str(li.append(html.A(anchor, href=router.url(href, strip_query=True), **kwargs)))
