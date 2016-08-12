"""PytSite Route Alias Event Handlers.
"""
from pytsite import router as _router
from . import _api, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_pre_dispatch(path_info: str):
    """'pytsite.router.pre_dispatch' event handler.
    """
    try:
        p = _api.get_by_alias(path_info)
        _router.add_path_alias(p.alias, p.target)
    except _error.RouteAliasNotFound:
        pass
