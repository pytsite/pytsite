"""Route Paths Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from pytsite.core.util import transform_str_1
from pytsite.core.lang import get_current_lang
from pytsite.core.odm import odm_manager
from .models import RouteAliasModel


def create(alias: str, target: str=None) -> RouteAliasModel:
    """Create a route alias instance.
    """
    entity = odm_manager.dispense('route_alias')
    entity.f_set('alias', alias)
    entity.f_set('target', target)
    entity.f_set('language', get_current_lang())

    return entity


def sanitize_alias_string(string: str) -> str:
    """Sanitize a path string.
    """
    string = transform_str_1(string)
    if not string:
        raise Exception('Alias cannot be empty.')

    if not string.startswith('/'):
        string = '/' + string

    itr = 0
    while True:
        if not odm_manager.find('route_alias').where('alias', '=', string).first():
            return string

        itr += 1
        if itr == 1:
            string += '-1'
        else:
            string = re.sub(r'-\d+$', '-' + str(itr), string)
