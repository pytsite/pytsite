from . import lang as __lang

__tags = dict()

__allowed_tags = {
    'title',
    'author',
    'description',
    'charset',
}


def set(tag: str, value: str):
    if tag not in __allowed_tags:
        raise Exception("Unknown tag '{0}'".format(tag))
    __tags[tag] = value


def set_multiple(tags: dict):
    """ Add multiple tags.
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

set('charset', 'UTF-8')
set('title', __lang.t('pytsite.core@untitled_document'))