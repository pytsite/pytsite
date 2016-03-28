"""PytSite Meta Tags Support.
"""
from pytsite import lang as _lang, util as _util, reg as _reg, events as _events, assetman as _assetman, \
    threading as _threading

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_tags = {}

_allowed_tags = (
    'title',
    'author',
    'link',
    'description',
    'charset',
    'viewport',
    'keywords',
    'og:title',
    'og:description',
    'og:locale',
    'og:image',
    'og:image:width',
    'og:image:height',
    'og:url',
    'og:type',
    'article:author',
    'article:publisher',
    'twitter:card',
    'twitter:title',
    'twitter:description',
    'twitter:image',
    'twitter:site',
    'fb:app_id',
    'fb:admins',
)


def reset():
    """Reset tags.
    """
    _tags[_threading.get_id()] = {'link': []}

    t_set('charset', 'UTF-8')
    t_set('title', _lang.t('pytsite.metatag@untitled_document'))
    t_set('viewport', 'width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0')
    t_set('link', rel='icon', type='image/png', href=_assetman.url(_reg.get('metatag.favicon.href')))


def t_set(tag: str, value: str=None, **kwargs):
    """Set tag value.
    """
    if tag not in _allowed_tags:
        raise Exception("Unknown tag '{}'".format(tag))

    tid = _threading.get_id()

    if tag in ('link',):
        if tag == 'link':
            if not kwargs.get('rel'):
                raise ValueError("<link> tag must contain 'rel' attribute")
            if not kwargs.get('href'):
                raise ValueError("<link> tag must contain 'href' attribute")

        value = ''
        for k, v in kwargs.items():
            value += ' {}="{}"'.format(k, v)

        _tags[tid]['link'].append(value)
    else:
        _tags[tid][tag] = _util.escape_html(value)


def get(tag: str) -> str:
    """Get value of the tag.
    """
    if tag not in _allowed_tags:
        raise Exception("Unknown tag '{0}'".format(tag))

    return _tags[_threading.get_id()].get(tag, '')


def dump(tag: str) -> str:
    """ Dump single tag.
    """
    if tag not in _allowed_tags:
        raise Exception("Unknown tag '{0}'".format(tag))

    tid = _threading.get_id()

    if tag not in _tags[tid]:
        return ''

    if tag == 'charset':
        r = '<meta charset="{}">\n'.format(_tags[tid][tag])
    elif tag == 'title':
        r = '<title>{} | {}</title>\n'.format(_tags[tid][tag], _lang.t('app_name'))
    elif tag.startswith('og:') or tag.startswith('author:') or tag.startswith('fb:'):
        r = '<meta property="{}" content="{}">'.format(tag, _tags[tid][tag])
    elif tag == 'link':
        r = ''
        for value in _tags[tid][tag]:
            r += '<{}{}>\n'.format(tag, value)
    else:
        r = '<meta name="{}" content="{}">'.format(tag, _tags[tid][tag])

    return r


def dump_all() -> str:
    """Dump all tags.
    """
    _events.fire('pytsite.metatag.dump_all')

    r = str()
    for tag in _tags[_threading.get_id()]:
        r += dump(tag) + '\n'

    return r
