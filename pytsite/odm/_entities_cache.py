"""PytSite Entities Cache.
"""
from pytsite import cache as _cache
from . import _entity

_entities_cache = _cache.create_pool('pytsite.odm.entities')


def has(model: str, eid: str) -> bool:
    return _entities_cache.has('{}:{}'.format(model, eid))


def get(model: str, eid: str) -> _entity.Entity:
    return _entities_cache.get('{}:{}'.format(model, eid))


def put(entity: _entity.Entity) -> _entity.Entity:
    if not entity.is_new:
        _entities_cache.put('{}:{}'.format(entity.model, str(entity.id)), entity)

    return entity


def rm(entity: _entity.Entity):
    _entities_cache.rm('{}:{}'.format(entity.model, str(entity.id)))
