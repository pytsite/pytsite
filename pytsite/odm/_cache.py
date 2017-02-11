"""PytSite ODM Cache.
"""
from datetime import datetime as _datetime
from pytsite import reg as _reg, logger as _logger

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_TTL = _reg.get('odm.cache.ttl', 1800)
_dbg = _reg.get('odm.cache.debug')
_entities = {}


def get(model: str, eid: str):
    """
    :rtype: pytsite.odm.model.Entity
    """
    entity = _entities['{}:{}'.format(model, eid)][0]

    if _dbg:
        _logger.debug("[ODM CACHE GET] '{}:{}'.".format(model, eid))

    return entity


def put(entity):
    """
    :param entity: pytsite.odm.model.Entity
    :rtype: pytsite.odm.model.Entity
    """
    c_key = '{}:{}'.format(entity.model, str(entity.id))

    if c_key in _entities:
        raise KeyError("Entity '{}' is already cached.".format(c_key))

    _entities[c_key] = (entity, _datetime.now())

    if _dbg:
        _logger.debug("[ODM CACHE PUT] '{}'.".format(c_key))
        _logger.debug("[ODM CACHE SIZE] {}.".format(len(_entities)))

    return entity


def remove(entity):
    """
    :param entity: pytsite.odm.model.Entity

    """
    if entity.is_new:
        raise RuntimeError('You cannot remove non-stored entities.')

    c_key = '{}:{}'.format(entity.model, entity.id)
    del _entities[c_key]

    if _dbg:
        _logger.debug("[ODM CACHE REMOVE] '{}'.".format(c_key))
        _logger.debug("[ODM CACHE SIZE] {}.".format(len(_entities)))


def cleanup():
    """Cleanup expired entities.
    """
    to_remove = []
    for i in _entities.values():
        if (_datetime.now() - i[1]).seconds > _TTL:
            to_remove.append(i[0])

    for i in to_remove:
        remove(i)


def get_size() -> int:
    """Get cache size.
    """
    return len(_entities)
