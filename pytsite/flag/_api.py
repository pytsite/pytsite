"""PytSite Flag API.
"""
from pytsite import odm as _odm, auth as _auth, cache as _cache, events as _events

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_CACHE_TTL = 300  # 5 min
_cache_p = _cache.create_pool('pytsite.flag')


def count(entity: _odm.model.Entity, flag_type: str = 'default') -> int:
    """Get flags count for the entity.
    """
    return _odm.find('flag').eq('entity', entity).eq('type', flag_type).count()


def sum(entity: _odm.model.Entity, flag_type: str = 'default') -> float:
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


def average(entity: _odm.model.Entity, flag_type: str = 'default') -> float:
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


def is_flagged(entity: _odm.model.Entity, author: _auth.model.AbstractUser = None, flag_type: str = 'default') -> bool:
    """Check if an entity is flagged by a user.
    """
    if not author:
        author = _auth.get_current_user()

    if author.is_anonymous:
        return False

    f = _odm.find('flag').eq('entity', entity).eq('author', author.uid).eq('type', flag_type)

    return bool(f.count())


def flag(entity: _odm.model.Entity, author: _auth.model.AbstractUser = None, flag_type: str = 'default',
         score: float = 1.0) -> int:
    """Flag the entity.
    """
    if not author:
        author = _auth.get_current_user()

    if author.is_anonymous:
        raise RuntimeError("Flag's author cannot be anonymous.")

    if is_flagged(entity, author):
        return

    e = _odm.dispense('flag')
    e.f_set('entity', entity).f_set('author', author.uid).f_set('type', flag_type).f_set('score', score)
    e.save()

    _events.fire('pytsite.flag.flag', entity=entity, user=author, flag_type=flag_type, score=score)

    return count(entity, flag_type)


def unflag(entity: _odm.model.Entity, author: _auth.model.AbstractUser = None, flag_type: str = 'default') -> int:
    """Remove flag.
    """
    if not author:
        author = _auth.get_current_user()

    if author.is_anonymous:
        raise RuntimeError("Flag's author cannot be anonymous.")

    if not is_flagged(entity, author):
        return

    f = _odm.find('flag').eq('entity', entity).eq('author', author.uid).eq('type', flag_type)
    fl = f.first()
    with fl:
        fl.delete()

    _events.fire('pytsite.flag.unflag', entity=entity, user=author, flag_type=flag_type)

    return count(entity, flag_type)


def toggle(entity: _odm.model.Entity, author: _auth.model.AbstractUser = None, flag_type: str = 'default',
           score: float = 1.0) -> int:
    """Toggle flag.
    """
    if not author:
        author = _auth.get_current_user()

    if author.is_anonymous:
        raise RuntimeError("Flag's author cannot be anonymous.")

    if is_flagged(entity, author, flag_type):
        return unflag(entity, author, flag_type)
    else:
        return flag(entity, author, flag_type, score)


def delete(entity: _odm.model.Entity) -> int:
    """Delete all flags for particular entity.
    """
    r = 0
    for flag_entity in _odm.find('flag').eq('entity', entity).get():
        with flag_entity:
            flag_entity.delete()
        r += 1

    return r
