__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

__tags = dict()
__allowed_tags = {
    'title',
    'author',
    'description',
    'charset',
}


def set_tag(tag: str, value: str):
    """Set tag value.
    """
    if tag not in __allowed_tags:
        raise Exception("Unknown tag '{0}'".format(tag))
    __tags[tag] = value


def set_multiple(tags: dict):
    """ Set multiple tags.
    """
    # TODO
    pass


def dump_tag(tag: str)->str:
    """ Dump single tag.
    """
    if tag not in __tags:
        raise Exception("Tag '{$tag}' is not registered")

    r = ''

    if tag not in __tags:
        return r

    if tag == 'charset':
        r = '<meta charset="{0}">\n'.format(__tags[tag])
    elif tag == 'title':
        r = '<title>{0}</title>\n'.format(__tags[tag])

    return r


def dump_all()->str:
    """Dump all tags.
    """
    r = str()
    for tag in __tags:
        r += dump_tag(tag)

    return r

# Minimum defaults
from . import lang as __lang
set_tag('charset', 'UTF-8')
set_tag('title', __lang.t('pytsite.core@untitled_document'))