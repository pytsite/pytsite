"""PytSite MetaTag Module.
"""
from ._functions import dump, dump_all, get, reset, t_set

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import lang, events

    lang.register_package(__name__)
    events.listen('pytsite.router.dispatch', reset)


__init()
