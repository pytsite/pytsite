"""Route Paths API.
"""
import re
from pytsite import util as _util, odm as _odm, lang as _lang
from . import _model, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def create(alias: str, target: str, language: str = None) -> _model.RouteAlias:
    """Create a route alias instance.
    """
    if not language:
        language = _lang.get_current()

    entity = _odm.dispense('route_alias')
    entity.f_set('language', language).f_set('alias', alias).f_set('target', target)

    return entity


def sanitize_alias_string(s: str, language: str = None) -> str:
    """Sanitize a path string.
    """
    s = _util.transform_str_1(s)

    if not language:
        language = _lang.get_current()

    if not s:
        raise RuntimeError('Alias cannot be empty.')

    if not s.startswith('/'):
        s = '/' + s

    itr = 0
    while True:
        if not _odm.find('route_alias').eq('alias', s).eq('language', language).first():
            return s

        itr += 1
        if itr == 1:
            s += '-1'
        else:
            s = re.sub('-\d+$', '-' + str(itr), s)


def find(language: str = None) -> _odm.Finder:
    """Get route alias finder.
    """
    return _odm.find('route_alias').eq('language', language or _lang.get_current())


def get_by_alias(alias: str, language: str = None) -> _model.RouteAlias:
    """Find route alias by target.
    """
    r_alias = find(language).eq('alias', alias).first()
    if not r_alias:
        raise _error.RouteAliasNotFound("Route alias for alias '{}', language '{}' not found.".format(alias, language))

    return r_alias


def get_by_target(target: str, language: str = None) -> _model.RouteAlias:
    """Find route alias by target.
    """
    r_alias = find(language).eq('target', target).first()
    if not r_alias:
        raise _error.RouteAliasNotFound("Route alias for target '{}', language '{}' not found.".
                                        format(target, language))

    return r_alias
