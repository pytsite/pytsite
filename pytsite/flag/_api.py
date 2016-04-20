"""PytSite Flag API.
"""
from pytsite import odm as _odm, auth as _auth, cache as _cache

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_CACHE_TTL = 1800  # 30 min
_cache_p = _cache.create_pool('pytsite.flag')


def count(entity: _odm.Entity, flag_type: str = 'default') -> int:
    """Get flags count for the entity.
    """
    return _odm.find('flag').where('entity', '=', entity).where('type', '=', flag_type).count()


def sum(entity: _odm.Entity, flag_type: str = 'default') -> float:
    """Get sum of scores for the entity.
    """
    c_key = 'sum.{}.{}'.format(entity.id, flag_type)
    if _cache_p.has(c_key):
        return _cache_p.get(c_key)

    ag = _odm.aggregate('flag').match('entity', '=', entity).match('type', '=', flag_type)

    ag.group({
        '_id': None,
        'sum': {'$sum': '$score'}
    })

    r = list(ag.get())
    v = r[0]['sum'] if r else 0.0

    return _cache_p.put(c_key, v, _CACHE_TTL)


def average(entity: _odm.Entity, flag_type: str = 'default') -> float:
    """Get average score for the entity.
    """
    c_key = 'average.{}.{}'.format(entity.id, flag_type)
    if _cache_p.has(c_key):
        return _cache_p.get(c_key)

    ag = _odm.aggregate('flag').match('entity', '=', entity).match('type', '=', flag_type)

    ag.group({
        '_id': None,
        'avg': {'$avg': '$score'}
    })

    r = list(ag.get())
    v = r[0]['avg'] if r else 0.0

    return _cache_p.put(c_key, v, _CACHE_TTL)


def is_flagged(entity: _odm.Entity, user: _auth.model.User, flag_type: str = 'default') -> bool:
    """Check if an entity is flagged by a user.
    """
    if user.is_anonymous:
        return False

    f = _odm.find('flag').where('entity', '=', entity).where('author', '=', user).where('type', '=', flag_type)

    return bool(f.count())


def flag(entity: _odm.Entity, author: _auth.model.User, flag_type: str = 'default', score: float = 1.0):
    """Flag the entity.
    """
    if author.is_anonymous:
        return

    if not is_flagged(entity, author):
        e = _odm.dispense('flag')
        e.f_set('entity', entity).f_set('author', author).f_set('type', flag_type).f_set('score', score)
        e.save()


def unflag(entity: _odm.Entity, author: _auth.model.User, flag_type: str = 'default'):
    """Remove flag.
    """
    if author.is_anonymous:
        return

    f = _odm.find('flag').where('entity', '=', entity).where('author', '=', author).where('type', '=', flag_type)
    f.first().delete()


def toggle(entity: _odm.Entity, author: _auth.model.User, flag_type: str = 'default', score: float = 1.0) -> bool:
    """Toggle flag.
    """
    if author.is_anonymous:
        return False

    if is_flagged(entity, author, flag_type):
        unflag(entity, author, flag_type)
        return False
    else:
        flag(entity, author, flag_type, score)
        return True


def delete(entity: _odm.Entity) -> int:
    """Delete all flags for particular entity.
    """
    r = 0
    for flag_entity in _odm.find('flag').where('entity', '=', entity).get():
        flag_entity.delete()
        r += 1

    return r
