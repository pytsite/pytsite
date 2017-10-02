"""PytSite Meta Tags
"""
from ._api import dump, dump_all, get, reset, t_set, rm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import lang, router, tpl

    lang.register_package(__name__)
    router.on_dispatch(reset, -999, '*')
    router.on_xhr_dispatch(reset, -999, '*')
    router.on_exception(lambda args: reset(args.get('title')), -999)

    tpl.register_global('metatag', dump)
    tpl.register_global('metatags', dump_all)
    tpl.register_global('metatag_get', get)


_init()
