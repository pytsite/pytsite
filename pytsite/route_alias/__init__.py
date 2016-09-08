"""Route Alias Package Init
"""
# Public API
from ._api import create, find, get_by_target, get_by_alias
from . import _model as model, _error as error


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import odm, events
    from . import _eh

    odm.register_model('route_alias', model.RouteAlias)
    events.listen('pytsite.router.pre_dispatch', _eh.router_pre_dispatch)


_init()
