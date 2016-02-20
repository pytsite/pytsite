"""PytSite ODM Finder Cache.
"""
from pytsite import cache as _cache, logger as _logger, reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def put(finder, result, ttl: int) -> tuple:
    """
    :param finder: pytsite.odm._finder.Finder
    :param result: pytsite.odm._finder.Result
    """
    pool_name = 'pytsite.odm.finder.' + finder.model

    if not _cache.has_pool(pool_name):
        _cache.create_pool(pool_name, default_ttl=ttl)

    r = tuple(result)
    _cache.get_pool(pool_name).put(finder.id, r, ttl)

    if _reg.get('odm.debug'):
        _logger.debug("PUT query results: query: {}, {}, id: {}, entities: {}, TTL: {}.".
                      format(finder.model, finder.query.compile(), finder.id, len(r), ttl), __name__)

    return r


def has(finder) -> bool:
    """
    :param finder: pytsite.odm._finder.Finder
    """
    pool_name = 'pytsite.odm.finder.' + finder.model

    if not _cache.has_pool(pool_name):
        return False

    item = _cache.get_pool(pool_name).get(finder.id)

    return True if item is not None else False


def get(finder) -> tuple:
    """
    :param finder: pytsite.odm._finder.Finder
    """
    pool_name = 'pytsite.odm.finder.' + finder.model

    if not has(finder):
        return

    r = _cache.get_pool(pool_name).get(finder.id)

    if _reg.get('odm.debug'):
        _logger.debug("GET query results: query: {}, {}, id: {}, entities: {}.".
                      format(finder.model, finder.query.compile(), finder.id, len(r)), __name__)

    return r


def clear(model: str):
    pool_name = 'pytsite.odm.finder.' + model

    if _cache.has_pool(pool_name):
        _cache.delete_pool(pool_name)
        if _reg.get('odm.debug'):
            _logger.debug("CLEAR pool: '{}'.".format(pool_name))
