"""Pytsite Disqus Package Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import comments, tpl, reg, events
    from . import _eh
    from ._comments import Driver

    if not reg.get('disqus.short_name'):
        raise ValueError("Configuration parameter 'disqus.short_name' is not defined.")

    if not reg.get('disqus.api_secret'):
        raise ValueError("Configuration parameter 'disqus.api_secret' is not defined.")

    tpl.register_package(__name__)
    comments.register_driver(Driver())

    events.listen('pytsite.update', _eh.pytsite_update)

__init()
