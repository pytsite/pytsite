"""PytSite Helper Functions.
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import random
import re
import pytz
import json
import dateparser
from importlib import reload as _importlib_reload
from os import path, makedirs, unlink, walk, listdir, rmdir
from tempfile import mkstemp, mkdtemp
from typing import Iterable, Union, List, Tuple
from frozendict import frozendict
from lxml import html as _lxml_html, etree as _lxml_etree
from time import tzname
from copy import deepcopy
from time import time
from datetime import datetime
from html import parser as python_html_parser
from hashlib import md5
from traceback import extract_stack
from werkzeug.utils import escape as wz_escape_html
from htmlmin import minify
from jsmin import jsmin
from urllib import request as urllib_request

_HTML_SCRIPT_RE = re.compile('(<script[^>]*>)([^<].+?)(</script>)', re.MULTILINE | re.DOTALL)
_MULTIPLE_SPACES_RE = re.compile('\s{2,}')
_HTML_SINGLE_TAGS = ('br', 'img', 'input')
_HTML_ALLOWED_EMPTY_TAGS = ('iframe',)
_LXML_HTML_PARSER = _lxml_etree.HTMLParser(encoding='utf-8', remove_blank_text=True, remove_comments=True)
_URL_RE = re.compile('^(?:http|ftp)s?://'  # Scheme
                     '(?:(?:[A-Z0-9](?:[A-Z0-9-_]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
                     'localhost|'  # localhost...
                     '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
                     '(?::\d+)?'  # optional port
                     '(?:/?|[/?]\S+)$', re.IGNORECASE)

_installed_packages = {}  # Installed pip packages cache


class _HTMLStripTagsParser(python_html_parser.HTMLParser):
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
        if self._safe_tags and tag in self._safe_tags and tag not in _HTML_SINGLE_TAGS:
            self._content.append('</{}>'.format(tag))

    def handle_data(self, data: str):
        self._content.append(data)

    def handle_entityref(self, name: str):
        self._content.append('&{};'.format(name))

    def handle_charref(self, name: str):
        self._content.append('&#{};'.format(name))

    def __str__(self) -> str:
        self.close()

        return ''.join(self._content)


class _HTMLTrimParser(python_html_parser.HTMLParser):
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
            if tag not in _HTML_SINGLE_TAGS:
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
    """Remove tags and attributes except safe_tags and empty tags which is should not be removed
    """
    safe_tags = 'a:href,target,rel|abbr|address|b|blockquote|br|cite|code:class|col|colgroup|dd|del|details|dfn|dl|' \
                'dt|em|figcaption|figure|h1:id|h2:id|h3:id|h4:id|h5:id|h6:id|hr|i|iframe:src,width,height|' \
                'img:src,alt|ins|kbd|li|mark|ol|output|p:style,id|param|pre:class|q|rt|ruby|s|samp|small|span|strong|' \
                'sub|summary|sup|table:style|tbody|td:style|tfoot|th|thead|time|tr|u|ul|var|wbr|header|footer'

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
            if item.tag not in _HTML_SINGLE_TAGS and item.tag not in _HTML_ALLOWED_EMPTY_TAGS and item.text:
                item_text = _MULTIPLE_SPACES_RE.sub(' ', item.text)
                if not item_text or item_text == ' ':
                    # Remove item with no text
                    item.getparent().remove(item)
                elif item.tag not in ('pre', 'code'):
                    # Put tidy text back to item
                    item.text = item_text

        return item

    s = strip_html_tags(s, safe_tags)

    if remove_empty_tags:
        # Remove tags while they present
        while True:
            s_xml = _empty_tags_cleaner(_lxml_html.fromstring(s, parser=_LXML_HTML_PARSER))
            s_cleaned = _lxml_html.tostring(s_xml, encoding='utf-8').decode('utf-8')

            # All done
            if s_cleaned == s:
                break

            s = s_cleaned

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
    return wz_escape_html(s)


def minify_html(s: str) -> str:
    """Minify an HTML string
    """

    def sub_f(m):
        g = m.groups()
        return ''.join((g[0], jsmin(g[1]), g[2])).replace('\n', '')

    return _HTML_SCRIPT_RE.sub(sub_f, minify(s, True, True, remove_optional_attribute_quotes=False))


def dict_merge(a: dict, b: dict) -> dict:
    """Recursively merge dicts.

    Not just simple a['key'] = b['key'], if both a and b have a key who's
    value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.
    https://www.xormedia.com/recursively-merge-dictionaries-in-python/"""

    if not isinstance(a, (dict, frozendict)) or not isinstance(b, (dict, frozendict)):
        raise TypeError('Expected both dictionaries as arguments')

    if isinstance(a, frozendict):
        a = dict(a)
    if isinstance(b, frozendict):
        b = dict(b)

    result = deepcopy(a)

    for k, v in b.items():
        if k in result:
            if isinstance(result[k], dict) and isinstance(v, dict):
                result[k] = dict_merge(result[k], v)
            elif isinstance(result[k], list) and isinstance(v, (set, list, tuple)):
                result[k].extend(v)
            elif isinstance(result[k], set) and isinstance(v, (set, list, tuple)):
                result[k].update(v)
            else:
                result[k] = deepcopy(v)
        else:
            result[k] = deepcopy(v)

    return result


def mk_tmp_file(suffix: str = None, prefix: str = None, subdir: str = None, text: bool = False) -> Tuple[int, str]:
    """Create temporary file

    Returns tuple of two items: file's descriptor and absolute path.
    """
    from pytsite import reg

    tmp_dir = reg.get('paths.tmp')
    if not tmp_dir:
        raise RuntimeError('Cannot determine temporary directory location')

    if subdir:
        tmp_dir = path.join(tmp_dir, subdir)

    if not path.exists(tmp_dir):
        makedirs(tmp_dir, 0o755)

    return mkstemp(suffix, prefix, tmp_dir, text)


def mk_tmp_dir(suffix: str = None, prefix: str = None, subdir: str = None) -> str:
    from pytsite import reg

    tmp_root = reg.get('paths.tmp')
    if not tmp_root:
        raise RuntimeError('Cannot determine temporary directory location')

    if subdir:
        tmp_root = path.join(tmp_root, subdir)

    if not path.exists(tmp_root):
        makedirs(tmp_root, 0o755)

    return mkdtemp(suffix, prefix, tmp_root)


def random_str(size: int = 16, alphabet: str = '0123456789abcdef', exclude: Iterable = None):
    """Generate random string.
    """
    while True:
        s = ''.join(random.choice(alphabet) for _ in range(size))
        if not exclude or s not in exclude:
            return s


def random_password(size: int = 16, alphanum_only: bool = False):
    """Generate random password.
    """
    alphabet = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if not alphanum_only:
        alphabet += '!@#$%^&*()_+=-`~|\\/.,?><{}[]":;'

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
                r += ' {}="{}"'.format(k, wz_escape_html(v))

    return r


def transform_str_1(s: str, language: str = None) -> str:
    """Transform a string, variant 1.

    1. Remove some "special" chars except slashes
    2. Lowercase
    3. Transliterate
    4. Replace multiple slashes with single ones
    5. Replace all non-alphanumeric chars with hyphens
    6. Replace multiple hyphens with single ones
    7. Remove leading and trailing hyphens
    """
    from pytsite import lang

    special_chars = (
        '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '=', '+', '"', "'", '{', '}', '[', ']', '`', '~', '|', '\\',
        '?', '.', ',', '<', '>', '«', '»', '№', ':', ';',
    )

    for c in special_chars:
        s = s.replace(c, '')

    s = lang.transliterate(s.lower(), language)
    s = re.sub('/{2,}', '/', s)
    s = re.sub('[^a-zA-Z0-9_/]', '-', s)
    s = re.sub('-{2,}', '-', s)
    s = re.sub('(^-|-$)', '', s)

    return s


def transform_str_2(s: str, language: str = None) -> str:
    """Transform a string, variant 2.

    1. transform_1()
    2. Replace slashes with hyphens
    """
    return transform_str_1(s, language).replace('/', '-')


def get_module_attr(s: str):
    """Resolve module attribute from dotted-notated name
    """
    class_fqn = cleanup_list(s.split('.'))
    if len(class_fqn) < 2:
        raise NameError("Cannot determine module attribute from '{}'.".format(s))

    attr_name = class_fqn[-1:][0]
    module_name = '.'.join(class_fqn[:-1])
    module_obj = __import__(module_name, fromlist=[attr_name])

    return getattr(module_obj, attr_name)


def cleanup_list(inp: Union[List, Tuple], uniquize: bool = False) -> list:
    """Remove empty values from a list.
    """
    if not isinstance(inp, (list, tuple)):
        TypeError('List or tuple expected.')

    r = []
    for v in inp:
        if isinstance(v, str):
            v = v.strip()
            if not v:
                continue

        if (uniquize and v not in r) or not uniquize:
            r.append(v)

    return r


def cleanup_dict(inp: dict) -> dict:
    """Remove empty values from a dict
    """
    r = {}
    for k, v in inp.items():
        if isinstance(v, str):
            v = v.strip()
        if v not in (None, ''):
            r[k] = v

    return r


def nav_link(url: str, anchor: str = '', icon: str = None, **kwargs) -> str:
    """Generate Bootstrap compatible navigation item link
    """
    from pytsite import html, router

    li = html.Li(css=kwargs.pop('li_css', 'nav-item'))

    if not url.startswith('#') and router.url(url, strip_query=True) == router.current_url(strip_query=True):
        li.add_css('active')

    a = html.A(escape_html(anchor), href=url, css=kwargs.pop('a_css', 'nav-link'), **kwargs)
    if icon:
        a.append(html.I(css=icon))

    li.append(a)

    return str(li)


def parse_date_time(s: str, date_formats: list = None, languages: list = None, locales: list = None,
                    region: str = None) -> datetime:
    """Parse a date/time string

    See docs at https://github.com/scrapinghub/dateparser
    """
    date = dateparser.parse(s, date_formats, languages, locales, region)
    if date is None:
        raise ValueError("'{}' is not a valid date/time string".format(s))

    return date


def rfc822_datetime_str(dt: datetime = None) -> str:
    """Format date/time string according to RFC-822 format
    """
    if not dt:
        dt = datetime.now()

    if not dt.tzinfo:
        dt = pytz.timezone(tzname[0]).localize(dt)

    return dt.strftime('%a, %d %b %Y %H:%M:%S %z')


def w3c_datetime_str(dt: datetime = None, date_only: bool = False) -> str:
    """Format date/time string according to W3C.
    """
    if not dt:
        dt = datetime.now()

    if not dt.tzinfo:
        dt = pytz.timezone(tzname[0]).localize(dt)

    return dt.strftime('%Y-%m-%d') if date_only else dt.strftime('%Y-%m-%dT%H:%M:%S%z')


def md5_hex_digest(inp, encoding='utf8') -> str:
    """Generates MD5 hex digest for string or bytes.
    """

    if isinstance(inp, str):
        inp = bytes(inp, encoding)

    m = md5()
    m.update(inp)

    return m.hexdigest()


def to_snake_case(s: str) -> str:
    """Convert CamelCase to snake_case.
    """
    s = re.sub('(.)([A-Z][a-z]+)', '\1_\2', s)
    return re.sub('([a-z0-9])([A-Z])', '\1_\2', s).lower()


def get_call_stack(limit: int = None) -> list:
    """Format call stack as string.
    """
    r = []
    for frame_sum in extract_stack(limit=limit):
        r.append([item for item in frame_sum[:3]])

    return r


def is_url(s: str) -> bool:
    """Check whether the string is an URL
    """
    return bool(_URL_RE.match(s))


def load_json(source: str):
    """Load JSON data from remote or local source
    """
    try:
        if is_url(source):
            with urllib_request.urlopen(source) as f:
                return json.load(f)
        else:
            with open(source) as f:
                return json.load(f)

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError("Error while loading JSON data from '{}': {}".format(source, e), e.doc, e.pos)


def cleanup_files(root_path: str, ttl: int) -> tuple:
    """Remove obsolete files and empty directories
    """
    now = time()
    success = []
    failed = []

    for root, d_names, f_names in walk(root_path):
        for f_name in f_names:
            f_path = path.join(root, f_name)
            m_time = path.getmtime(f_path)
            if m_time + ttl < now:
                try:
                    unlink(f_path)
                    success.append(f_path)

                except Exception as e:
                    failed.append((f_path, e))

        # Remove empty directories
        for d_name in d_names:
            d_path = path.join(root, d_name)
            if not listdir(d_path):
                rmdir(d_path)

    return success, failed


def reload_module(module, _package: str = None, _reloaded: list = None):
    """Recursively reload a module
    """
    if not hasattr(module, '__package__'):
        raise TypeError('Is not a module: {}'.format(module))

    if not _package:
        _package = module.__package__

    if not _reloaded:
        _reloaded = []

    mod_id = id(module)

    if mod_id in _reloaded:
        return

    # Reload the module
    _reloaded.append(mod_id)
    _importlib_reload(module)

    # Reload submodules
    for attr_name in dir(module):
        attr = getattr(module, attr_name)

        # Attribute is not a module
        if not hasattr(attr, '__package__'):
            continue

        # Module is not belongs to the current package
        if not attr.__package__.startswith(_package):
            continue

        # Module is a package
        reload_module(attr, _package, _reloaded)
