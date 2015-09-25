"""Flag Package Functions.
"""
from pytsite import odm as _odm, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def flag(entity: _odm.Model, author: _auth.model.User=None):
    if not author:
        author = _auth.get_current_user()

    if author.is_anonymous:
        raise ValueError('Author cannot be anonymous.')

    if not count(entity, author):
        _odm.dispense('flag').f_set('entity', entity).f_set('author', author).save()


def count(entity: _odm.Model, author: _auth.model.User=None) -> int:
    f = _odm.find('flag').where('entity', '=', entity)

    if author and not author.is_anonymous:
        f.where('author', '=', entity)

    return f.count()


def delete(entity: _odm.Model, author: _auth.model.User=None):
    f = _odm.find('flag').where('entity', '=', entity)

    if author and not author.is_anonymous:
        f.where('author', '=', entity)

    for e in f.get():
        e.delete()
