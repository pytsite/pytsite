"""PytSite Meta Tags Support.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from .lang import t

__tags = {
    'charset': 'UTF-8',
    'title': t('pytsite.core@untitled_document'),
    'viewport': 'width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0',
}
__allowed_tags = (
    'title',
    'author',
    'description',
    'charset',
    'viewport',
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
        r = '<title>{} | {}</title>\n'.format(__tags[tag], t('app_name'))
    else:
        r = '<meta name="{}" content="{}">'.format(tag, __tags[tag])

    return r


def dump_all() -> str:
    """Dump all tags.
    """
    r = str()
    for tag in __tags:
        r += dump(tag)

    return r
