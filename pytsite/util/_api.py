"""PytSite Helper Functions.
"""
import random as _random
import re as _re
import pytz as _pytz
from typing import Iterable as _Iterable, Union as _Union, List as _List, Tuple as _Tuple
from importlib import import_module as _import_module
from lxml import html as _lxml_html, etree as _lxml_etree
from time import tzname as _tzname
from copy import deepcopy as _deepcopy
from datetime import datetime as _datetime
from html import parser as _python_html_parser
from hashlib import md5 as _md5
from traceback import extract_stack as _extract_stack
from werkzeug.utils import escape as _escape_html
from htmlmin import minify as _minify
from jsmin import jsmin as _jsmin

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_html_script_re = _re.compile('(<script[^>]*>)([^<].+?)(</script>)', _re.MULTILINE | _re.DOTALL)
_html_single_tags = ('br', 'img', 'input')
_html_allowed_empty_tags = ('iframe',)
_lxml_etree_html_parser = _lxml_etree.HTMLParser(encoding='utf-8', remove_blank_text=True, remove_comments=True)


class _HTMLStripTagsParser(_python_html_parser.HTMLParser):
    def __init__(self, safe_tags: str = None):
        """
        :param safe_tags: safe tags and attributes, i. e. 'a:href,rel|img:src,alt|p:class,lang'
        """
        super().__init__(convert_charrefs=False)
        self._safe_tags = None
        self._content = []

        if safe_tags:
            self._safe_tags = {}
            for safe_tag_data in safe_tags.split('|'):
                safe_tag_data_split = safe_tag_data.split(':')
                if len(safe_tag_data_split) == 1:
                    self._safe_tags[safe_tag_data_split[0]] = []
                else:
                    self._safe_tags[safe_tag_data_split[0]] = safe_tag_data_split[1].split(',')

    def error(self, message):
        raise RuntimeError(message)

    def handle_starttag(self, tag, attrs):
        if not self._safe_tags or tag not in self._safe_tags:
            return

        attrs_to_add = []
        for attr in attrs:
            if attr[0] not in self._safe_tags[tag]:
                continue
            if attr[1]:
                attrs_to_add.append('{}="{}"'.format(attr[0], attr[1]))
            else:
                attrs_to_add.append('{}'.format(attr[0]))

        if attrs_to_add:
            self._content.append('<{} {}>'.format(tag, ' '.join(attrs_to_add)))
        else:
            self._content.append('<{}>'.format(tag))

    def handle_endtag(self, tag):
        if self._safe_tags and tag in self._safe_tags and tag not in _html_single_tags:
            self._content.append('</{}>'.format(tag))

    def handle_data(self, data: str):
        self._content.append(data)

    def handle_entityref(self, name: str):
        self._content.append('&{};'.format(name))

    def handle_charref(self, name: str):
        self._content.append('&#{};'.format(name))

    def __str__(self) -> str:
        self.close()

        return _re.sub(' {2,}', ' ', ''.join(self._content))


class _HTMLTrimParser(_python_html_parser.HTMLParser):
    def __init__(self, limit: int, count_bytes: bool = False):
        super().__init__(convert_charrefs=False)

        self._limit = limit
        self._count_bytes = count_bytes
        self._str = ''
        self._tags_stack = []

    def error(self, message):
        raise RuntimeError(message)

    def handle_starttag(self, tag: str, attrs: list):
        if not self._get_available_len():
            return

        tag_str = '<{}'.format(tag)

        attrs_str = []
        for a in attrs:
            if a[1]:
                attrs_str.append('{}="{}"'.format(a[0], escape_html(a[1].replace('"', "'"))))
            else:
                attrs_str.append(a[0])
        if attrs_str:
            tag_str += ' {}'.format(' '.join(attrs_str))
        tag_str += '>'

        tag_str_len = len(tag_str.encode()) if self._count_bytes else len(tag_str)
        if self._get_available_len() >= tag_str_len:
            self._str += tag_str
            if tag not in _html_single_tags:
                self._tags_stack.append(tag)

    def handle_endtag(self, tag: str):
        if self._tags_stack:
            self._str += '</{}>'.format(self._tags_stack.pop())

    def handle_data(self, data: str):
        if not self._get_available_len():
            return

        for char in data:
            char_len = len(char.encode()) if self._count_bytes else len(char)
            if self._get_available_len() >= char_len:
                self._str += char

    def handle_entityref(self, name: str):
        if not self._get_available_len():
            return

        if len(name) + 2 <= self._get_available_len():
            self._str += '&{};'.format(name)

    def handle_charref(self, name: str):
        if not self._get_available_len():
            return

        if len(name) + 2 <= self._get_available_len():
            self._str += '&{};'.format(name)

    def _get_available_len(self) -> int:
        closing_tags_len = 0
        for tag in self._tags_stack:
            tag_str = '</{}>'.format(tag)
            closing_tags_len += len(tag_str.encode()) if self._count_bytes else len(tag_str)

        self_str_len = len(self._str.encode()) if self._count_bytes else len(self._str)

        return self._limit - self_str_len - closing_tags_len

    def __str__(self) -> str:
        self.close()

        # Closing all non-closed tags
        while self._tags_stack:
            self._str += '</{}>'.format(self._tags_stack.pop())

        return self._str


def strip_html_tags(s: str, safe_tags: str = None) -> str:
    """Strip HTML tags from a string.
    """
    parser = _HTMLStripTagsParser(safe_tags)
    parser.feed(s)

    return str(parser)


def tidyfy_html(s: str, remove_empty_tags: bool = True, add_safe_tags: str = None, remove_tags: str = None) -> str:
    """Remove tags and attributes except safe_tags and empty tags is necessary.
    """
    safe_tags = 'a:href:target:rel|abbr|address|b|blockquote|br|cite|code:class|col|colgroup|dd|del|details|dfn|dl|' \
                'dt|em|figcaption|figure|h1|h2|h3|h4|h5|h6|hr|i|iframe:src:width:height|img:src:alt|ins|kbd|li|mark|' \
                'ol|output|p|param|pre:class|q|rt|ruby|s|samp|small|span|strong|sub|summary|sup|table|tbody|td|' \
                'tfoot|th|thead|time|tr|u|ul|var|wbr'

    if remove_tags:
        for remove_tag in remove_tags.split('|'):
            st = [v for v in safe_tags.split('|') if v != remove_tag and not v.startswith(remove_tag + ':')]
            safe_tags = '|'.join(st)

    if add_safe_tags:
        safe_tags += '|' + add_safe_tags

    def _empty_tags_cleaner(item):
        # If the element has children, deep into it and parse children
        if len(item):
            for child in item:
                _empty_tags_cleaner(child)
        # If the element has NO children, check its text content
        else:
            if item.tag not in _html_single_tags and item.tag not in _html_allowed_empty_tags and item.text:
                item_text = item.text.strip()
                if not item_text:
                    # Remove item with no text
                    item.getparent().remove(item)
                else:
                    # Put tidy text back to item
                    item.text = item_text

        return item

    s = strip_html_tags(s, safe_tags)

    if remove_empty_tags:
        # Remove tags while they present
        while True:
            s_xml = _empty_tags_cleaner(_lxml_html.fromstring(s, parser=_lxml_etree_html_parser))
            s_cleaned = _lxml_html.tostring(s_xml, encoding='utf-8').decode('utf-8')
            if s_cleaned == s:
                break

            s = s_cleaned

        s = _re.sub(' {2,}', ' ', s)

        # Remove root '<div>' tag which can be added by lxml
        if s.startswith('<div>'):
            s = s[5:-6]

    return s


def trim_str(s: str, limit: int = 140, count_bytes: bool = False) -> str:
    """Trims ordinary or HTML string to the specified length.
    """
    parser = _HTMLTrimParser(limit, count_bytes)
    parser.feed(s)

    return str(parser)


def escape_html(s: str) -> str:
    """Escape an HTML string.
    """
    return _escape_html(s)


def minify_html(s: str) -> str:
    """Minify an HTML string.
    """

    def sub_f(m):
        g = m.groups()
        return ''.join((g[0], _jsmin(g[1]), g[2])).replace('\n', '')

    return _html_script_re.sub(sub_f, _minify(s, True, True, remove_optional_attribute_quotes=False))


def dict_merge(a: dict, b: dict) -> dict:
    """Recursively merge dicts.

    Not just simple a['key'] = b['key'], if both a and b have a key who's
    value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.
    https://www.xormedia.com/recursively-merge-dictionaries-in-python/"""

    if not isinstance(a, dict) or not isinstance(b, dict):
        raise TypeError('Expected both dictionaries as arguments.')

    result = _deepcopy(a)

    for k, v in b.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
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
        raise RuntimeError("Cannot determine temporary directory location.")

    if not path.exists(tmp_dir):
        mkdir(tmp_dir)

    return mkstemp(dir=tmp_dir)


def random_str(size=16, alphabet='0123456789abcdef', exclude: _Iterable = None):
    """Generate random string.
    """
    while True:
        s = ''.join(_random.choice(alphabet) for _ in range(size))
        if not exclude or s not in exclude:
            return s


def random_password(size=16):
    """Generate random password.
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-`~|\/.,?><{}[]":;'
    return random_str(size, alphabet)


def weight_sort(inp: list, key: str = 'weight') -> list:
    """Sort list by weight.
    """
    return sorted(inp, key=lambda x: getattr(x, key) if hasattr(x, key) else x[key])


def html_attrs_str(attrs: dict, replace_keys: dict = None) -> str:
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


def transliterate(text: str) -> str:
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

    1. Remove some "special" chars except slashes
    2. Lowercase
    3. Transliterate
    4. Replace multiple slashes with single ones
    5. Replace all non-alphanumeric chars with hyphens
    6. Replace multiple hyphens with single ones
    7. Remove leading and trailing hyphens
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

    1. transform_1()
    2. Replace slashes with hyphens
    """
    return _re.sub('/', '-', transform_str_1(s))


def get_class(s: str) -> type:
    """Get class by its dotted-notation name.
    """
    if not isinstance(s, str):
        raise ValueError('String expected.')

    class_fqn = cleanup_list(s.split('.'))
    if len(class_fqn) < 2:
        raise NameError("Cannot determine class name from string '{}'.".format(s))

    class_name = class_fqn[-1:][0]
    module_name = '.'.join(class_fqn[:-1])
    module = __import__(module_name, fromlist=[class_name])

    return getattr(module, class_name)


def cleanup_list(inp: _Union[_List, _Tuple], uniquize: bool = False) -> list:
    """Remove empty values from a list.
    """
    if not isinstance(inp, (list, tuple)):
        TypeError('List or tuple expected.')

    r = []
    for v in inp:
        if isinstance(v, str):
            v = v.strip()

        if v and ((uniquize and v not in r) or not uniquize):
            r.append(v)

    return r


def cleanup_dict(inp: dict) -> dict:
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


def nav_link(url: str, anchor: str = '', icon: str = None, **kwargs) -> str:
    """Generate Bootstrap compatible navigation item link.
    """
    from pytsite import html, router

    li = html.Li()

    if not url.startswith('#') and router.url(url, strip_query=True) == router.current_url(strip_query=True):
        li.set_attr('cls', 'active')

    a = html.A(escape_html(anchor), href=url, **kwargs)
    if icon:
        a.append(html.I(cls=icon))

    li.append(a)

    return str(li)


def parse_rfc822_datetime_str(s: str) -> _datetime:
    """Parse date/time string according to RFC-822.
    """
    try:
        # Year with century
        return _datetime.strptime(s, '%a, %d %b %Y %H:%M:%S %z')

    except ValueError:
        # Year without century
        return _datetime.strptime(s, '%a, %d %b %y %H:%M:%S %z')


def rfc822_datetime_str(dt: _datetime = None) -> str:
    """Format date/time string according to RFC-822.
    """
    if not dt:
        dt = _datetime.now()

    if not dt.tzinfo:
        dt = _pytz.timezone(_tzname[0]).localize(dt)

    return dt.strftime('%a, %d %b %Y %H:%M:%S %z')


def w3c_datetime_str(dt: _datetime = None, date_only: bool = False) -> str:
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


def to_snake_case(s: str) -> str:
    """Convert CamelCase to snake_case.
    """
    s = _re.sub('(.)([A-Z][a-z]+)', r'\1_\2', s)
    return _re.sub('([a-z0-9])([A-Z])', r'\1_\2', s).lower()


def get_callable(s: str) -> callable:
    """Check if the object described by a string is callable.
    """
    s = s.split('.')

    module_name = '.'.join(s[:-1])
    callable_name = ''.join(s[-1:])

    module = _import_module(module_name)
    if callable_name not in dir(module):
        raise ImportError("Module '{}' doesn't define '{}'".format(module_name, callable_name))

    callable_obj = getattr(module, callable_name)
    if not callable(callable_obj):
        raise ImportError("Object '{}' of module '{}' is not callable".format(callable_name, module_name))

    return callable_obj


def format_call_stack_str(sep: str = '\n', skip: int = 1, limit: int = None) -> str:
    """Format call stack as string.
    """
    r = []
    for frame_sum in _extract_stack(limit=limit)[:-skip]:
        r.append(':'.join([str(item) for item in frame_sum[:3]]))

    return sep.join(r)
