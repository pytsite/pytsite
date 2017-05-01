"""PytSite Meta Tags Support.
"""
from pytsite import lang as _lang, util as _util, events as _events, assetman as _assetman, \
    threading as _threading

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_tags = {}


def reset(title: str = None):
    """Reset tags.
    """
    tid = _threading.get_id()
    _tags[tid] = {}

    t_set('charset', 'UTF-8')
    t_set('title', title or _lang.t('pytsite.metatag@untitled_document'))
    t_set('viewport', 'width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0')
    t_set('link', rel='icon', type='image/png', href=_assetman.url('$theme@img/favicon.png'))


def t_set(tag: str, value: str = None, **kwargs):
    """Set tag's value.
    """
    if not _tags:
        raise RuntimeError('reset() should be called before')

    tid = _threading.get_id()

    if tag not in _tags[tid]:
        _tags[tid][tag] = [] if tag == 'link' else ''

    if tag == 'link':
        _tags[tid][tag].append(kwargs)
    else:
        _tags[tid][tag] = _util.escape_html(value)


def get(tag: str) -> str:
    """Get value of the tag.
    """
    if not _tags:
        raise RuntimeError('reset() should be called before')

    return _tags[_threading.get_id()].get(tag, '')


def rm(tag: str, **kwargs):
    tid = _threading.get_id()
    if tid not in _tags or tag not in _tags[tid]:
        return

    if tag == 'link':
        if not _tags[tid][tag]:
            return

        values_to_rm = []
        for v in _tags[tid][tag]:
            if set(kwargs.items()).issubset(set(v.items())):
                values_to_rm.append(v)

        for v in values_to_rm:
            _tags[tid][tag].remove(v)

    else:
        del _tags[tid][tag]


def dump(tag: str) -> str:
    """ Dump single tag.
    """
    if not _tags:
        raise RuntimeError('reset() should be called before')

    tid = _threading.get_id()

    if tag not in _tags[tid]:
        return ''

    # Page charset
    if tag == 'charset':
        r = '<meta charset="{}">\n'.format(_tags[tid][tag])

    # Page title
    elif tag == 'title':
        r = '<title>{} | {}</title>\n'.format(_tags[tid][tag], _lang.t('app@app_name'))

    # OpenGraph tags
    elif tag.startswith('og:') or tag.startswith('author:') or tag.startswith('fb:'):
        r = '<meta property="{}" content="{}">'.format(tag, _tags[tid][tag])

    # Page links
    elif tag == 'link':
        r = ''
        for value in _tags[tid][tag]:
            args_str = ' '.join(['{}="{}"'.format(k, v) for k, v in value.items()])
            r += '<{} {}>\n'.format(tag, args_str)

    # Other
    else:
        r = '<meta name="{}" content="{}">'.format(tag, _tags[tid][tag])

    return r


def dump_all() -> str:
    """Dump all tags.
    """
    if not _tags:
        raise RuntimeError('reset() should be called before')

    _events.fire('pytsite.metatag.dump_all')

    r = str()
    for tag in _tags[_threading.get_id()]:
        r += dump(tag) + '\n'

    return r
