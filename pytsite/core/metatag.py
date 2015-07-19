"""PytSite Meta Tags Support.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from . import lang as _lang


__tags = {
    'charset': 'UTF-8',
    'title': _lang.t('core@untitled_document'),
    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0',
}
__allowed_tags = (
    'title',
    'author',
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
    'twitter:card',
    'twitter:title',
    'twitter:description',
    'twitter:image',
)


def t_set(tag: str, value: str):
    """Set tag value.
    """
    if tag not in __allowed_tags:
        raise Exception("Unknown tag '{0}'".format(tag))

    __tags[tag] = value


def t_set_multiple(tags: dict):
    """ Set multiple tags.
    """
    # TODO
    pass


def get(tag: str) -> str:
    """Get value of the tag.
    """
    if tag not in __allowed_tags:
        raise Exception("Unknown tag '{0}'".format(tag))

    if tag not in __tags:
        return ''

    return __tags[tag]


def dump(tag: str) -> str:
    """ Dump single tag.
    """
    r = ''

    if tag == 'charset':
        r = '<meta charset="{}">\n'.format(__tags[tag])
    elif tag == 'title':
        r = '<title>{} | {}</title>\n'.format(__tags[tag], _lang.t('app_name'))
    elif tag.startswith('og:'):
        r = '<meta property="{}" content="{}">'.format(tag, __tags[tag])
    else:
        r = '<meta name="{}" content="{}">'.format(tag, __tags[tag])

    return r


def dump_all() -> str:
    """Dump all tags.
    """
    r = str()
    for tag in __tags:
        r += dump(tag) + '\n'

    return r
