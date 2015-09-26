"""Flag Package Functions.
"""
from pytsite import odm as _odm, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def count(entity: _odm.Model) -> int:
    """Get overall flags count for this entity.
    """
    return _odm.find('flag').where('entity', '=', entity).count()


def is_flagged(entity: _odm.Model, author: _auth.model.User) -> bool:
    if author.is_anonymous:
        return False

    return bool(_odm.find('flag').where('entity', '=', entity).where('author', '=', author).count())


def flag(entity: _odm.Model, author: _auth.model.User):
    if author.is_anonymous:
        return

    if not is_flagged(entity, author):
        _odm.dispense('flag').f_set('entity', entity).f_set('author', author).save()


def unflag(entity: _odm.Model, author: _auth.model.User):
    if author.is_anonymous:
        return

    _odm.find('flag').where('entity', '=', entity).where('author', '=', author).first().delete()


def toggle(entity: _odm.Model, author: _auth.model.User) -> bool:
    """Toggle flag for the entity.
    """
    if author.is_anonymous:
        return False

    if is_flagged(entity, author):
        unflag(entity, author)
        return False
    else:
        flag(entity, author)
        return True


def delete(entity: _odm.Model):
    """Delete all the flags for particular entity.
    """
    for entity in _odm.find('flag').where('entity', '=', entity).get():
        entity.delete()
