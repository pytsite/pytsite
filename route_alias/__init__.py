"""Path Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import events, router, lang
from pytsite.core.odm import odm_manager
from .models import RouteAliasModel


def router_pre_dispatch_handler(path_info: str):
    """Router pre-dispatch event handler.
    """
    p = odm_manager.find('route_alias')\
        .where('alias', '=', path_info)\
        .where('language', '=', lang.get_current_lang())\
        .first()

    if p:
        router.add_path_alias(p.f_get('alias'), p.f_get('target'))

events.listen('pytsite.core.router.pre_dispatch', router_pre_dispatch_handler)

odm_manager.register_model('route_alias', RouteAliasModel)
