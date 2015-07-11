"""Route Paths Manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import re
from pytsite.core import util as _util, lang as _lang, odm as _odm
from . import _model


def create(alias: str, target: str=None) -> _model.RouteAlias:
    """Create a route alias instance.
    """
    entity = _odm.dispense('route_alias')
    entity.f_set('alias', alias)
    entity.f_set('target', target)
    entity.f_set('language', _lang.get_current_lang())

    return entity


def sanitize_alias_string(string: str) -> str:
    """Sanitize a path string.
    """
    string = _util.transform_str_1(string)
    if not string:
        raise Exception('Alias cannot be empty.')

    if not string.startswith('/'):
        string = '/' + string

    itr = 0
    while True:
        if not _odm.find('route_alias').where('alias', '=', string).first():
            return string

        itr += 1
        if itr == 1:
            string += '-1'
        else:
            string = re.sub(r'-\d+$', '-' + str(itr), string)

def find_by_target(target: str) -> _model.RouteAlias:
    """Find route alias by target.
    """
    lng = _lang.get_current_lang()
    return _odm.find('route_alias').where('target', '=', target).where('language', '=', lng).first()
