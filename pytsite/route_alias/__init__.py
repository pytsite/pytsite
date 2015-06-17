"""Route Alias Package Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __router_pre_dispatch_handler(path_info: str):
    """Router pre-dispatch event handler.
    """
    from pytsite.core import odm, lang, router
    p = odm.manager.find('route_alias')\
        .where('alias', '=', path_info)\
        .where('language', '=', lang.get_current_lang())\
        .first()

    if p:
        router.add_path_alias(p.f_get('alias'), p.f_get('target'))

def __init():
    from pytsite.core import events, odm
    from ._model import RouteAliasModel
    events.listen('pytsite.core.router.pre_dispatch', __router_pre_dispatch_handler)
    odm.manager.register_model('route_alias', RouteAliasModel)


__init()


# Public API
from . import _manager, _model
manager = _manager
model = _model
