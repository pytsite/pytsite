"""Route Paths API.
"""
import re
from pytsite import util as _util, odm as _odm, lang as _lang
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def create(alias: str, target: str, language: str=None) -> _model.RouteAlias:
    """Create a route alias instance.
    """
    if not language:
        language = _lang.get_current()

    entity = _odm.dispense('route_alias')
    entity.f_set('language', language).f_set('alias', alias).f_set('target', target)

    return entity


def sanitize_alias_string(s: str, language: str=None) -> str:
    """Sanitize a path string.
    """
    s = _util.transform_str_1(s)

    if not language:
        language = _lang.get_current()

    if not s:
        raise Exception('Alias cannot be empty.')

    if not s.startswith('/'):
        s = '/' + s

    itr = 0
    while True:
        if not _odm.find('route_alias').where('alias', '=', s).where('language', '=', language).first():
            return s

        itr += 1
        if itr == 1:
            s += '-1'
        else:
            s = re.sub('-\d+$', '-' + str(itr), s)


def find() -> _odm.Finder:
    """Get route alias finder.
    """
    return _odm.find('route_alias').where('language', '=', _lang.get_current())


def find_by_alias(alias: str, language: str=None) -> _model.RouteAlias:
    """Find route alias by target.
    """
    if not language:
        language = _lang.get_current()

    return _odm.find('route_alias').where('alias', '=', alias).where('language', '=', language).first()


def find_by_target(target: str, language: str=None) -> _model.RouteAlias:
    """Find route alias by target.
    """
    if not language:
        language = _lang.get_current()

    return _odm.find('route_alias').where('target', '=', target).where('language', '=', language).first()
