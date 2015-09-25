"""Route Alias Package Init
"""
from pytsite import odm as _odm, lang as _lang, router as _router, events as _events

# Public API
from . import _model as model
from ._api import create, find, find_by_target, find_by_alias

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __router_pre_dispatch_handler(path_info: str):
    """Router pre-dispatch event handler.
    """
    p = _odm.find('route_alias') \
        .where('alias', '=', path_info) \
        .where('language', '=', _lang.get_current_lang()) \
        .first()

    if p:
        _router.add_path_alias(p.f_get('alias'), p.f_get('target'))


def __init():
    from ._model import RouteAlias
    _events.listen('pytsite.router.pre_dispatch', __router_pre_dispatch_handler)
    _odm.register_model('route_alias', RouteAlias)


__init()
