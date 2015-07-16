"""Route Alias Package Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __router_pre_dispatch_handler(path_info: str):
    """Router pre-dispatch event handler.
    """
    from pytsite.core import odm, lang, router
    p = odm.find('route_alias') \
        .where('alias', '=', path_info) \
        .where('language', '=', lang.get_current_lang()) \
        .first()

    if p:
        router.add_path_alias(p.f_get('alias'), p.f_get('target'))


def __init():
    from pytsite.core import events, odm
    from ._model import RouteAlias
    events.listen('pytsite.core.router.pre_dispatch', __router_pre_dispatch_handler)
    odm.register_model('route_alias', RouteAlias)


__init()


# Public API
from . import _model as model
from ._manager import find, find_one_by_target, create
