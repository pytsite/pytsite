"""PytSite Helper Functions.
"""
import random as _random
import re as _re
import pytz as _pytz
from time import tzname as _tzname
from copy import deepcopy as _deepcopy
from datetime import datetime as _datetime
from html import parser as _html_parser
from hashlib import md5 as _md5
from werkzeug.utils import escape as _escape_html


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class _HTMLStripTagsParser(_html_parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self._data = []

    def error(self, message):
        raise Exception(message)

    def handle_data(self, data: str):
        data = _re.sub(r'\n', ' ', data, flags=_re.MULTILINE)
        data = _re.sub(r'\s{2,}', ' ', data)

        self._data.append(data)

    def __str__(self) -> str:
        return ' '.join(self._data)


def strip_html_tags(s: str) -> str:
    """Strips HTML tags from a string.
    """
    parser = _HTMLStripTagsParser()
    parser.feed(s)

    return str(parser)


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
    def f_sort(x):
        return getattr(x, key) if hasattr(x, key) else x[key]

    return sorted(inp, key=f_sort)


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
    if not isinstance(s, str):
        raise ValueError('String expected.')

    class_fqn = list_cleanup(s.split('.'))
    if len(class_fqn) < 2:
        raise NameError("Cannot determine class name from string '{}'.".format(s))

    class_name = class_fqn[-1:][0]
    module_name = '.'.join(class_fqn[:-1])
    module = __import__(module_name, fromlist=[class_name])

    return getattr(module, class_name)


def list_cleanup(inp: list) -> list:
    """Remove empty strings from a list.
    """
    r = []
    for v in inp:
        if isinstance(v, str):
            v = v.strip()
            if v:
                r.append(v)
        else:
            r.append(v)

    return r


def dict_cleanup(inp: dict) -> dict:
    """Remove empty strings from dict.
    """
    r = {}
    for k, v in inp.items():
        if isinstance(v, str):
            v = v.strip()
            if v:
                r[k] = v
        else:
            r[k] = v

    return r


def nav_link(url: str, anchor: str, **kwargs) -> str:
    """Generate Bootstrap compatible navigation item link.
    """
    from pytsite import html, router

    li = html.Li()

    if not url.startswith('#') and router.url(url, strip_query=True) == router.current_url(strip_query=True):
        li.set_attr('cls', 'active')

    li.append(html.A(anchor, href=url, **kwargs))

    return str(li)


def rfc822_datetime(dt: _datetime=None) -> str:
    """Format date/time string according to RFC-822.
    """
    if not dt:
        dt = _datetime.now()

    if not dt.tzinfo:
        dt = _pytz.timezone(_tzname[0]).localize(dt)

    return dt.strftime('%a, %d %b %Y %H:%M:%S %z')


def w3c_datetime(dt: _datetime=None, date_only: bool=False) -> str:
    """Format date/time string according to W3C.
    """
    if not dt:
        dt = _datetime.now()

    if not dt.tzinfo:
        dt = _pytz.timezone(_tzname[0]).localize(dt)

    return dt.strftime('%Y-%m-%d') if date_only else dt.strftime('%Y-%m-%dT%H:%M:%S%z')


def md5_hex_digest(inp, encoding='utf8') -> str:
    """Generates MD5 hex digest for string or bytes.

    :type inp: bytes | str
    """

    if isinstance(inp, str):
        inp = bytes(inp, encoding)

    m = _md5()
    m.update(inp)

    return m.hexdigest()
