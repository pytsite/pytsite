"""PytSite ODM Cache.
"""
from pytsite import reg as _reg, logger as _logger

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_entities = {}
_dbg = _reg.get('odm.debug.cache')


def get(model: str, eid: str):
    """
    :rtype: pytsite.odm.model.Entity
    """
    entity = _entities['{}:{}'.format(model, eid)]

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
        raise KeyError("Entity '{}' is already cached.")

    _entities[c_key] = entity

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
