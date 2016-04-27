"""Route Alias Package Init
"""
from pytsite import odm as _odm, router as _router, events as _events

# Public API
from . import _model as model
from ._api import create, find, find_by_target, find_by_alias

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _router_pre_dispatch_handler(path_info: str):
    """Router pre-dispatch event handler.
    """
    p = find_by_alias(path_info)
    if p:
        _router.add_path_alias(p.f_get('alias'), p.f_get('target'))


def __init():
    from ._model import RouteAlias
    _events.listen('pytsite.router.pre_dispatch', _router_pre_dispatch_handler)
    _odm.register_model('route_alias', RouteAlias)


__init()
