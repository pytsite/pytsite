"""Flag Package Functions.
"""
from pytsite import odm as _odm

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def count(uid: str) -> int:
    return _odm.find('flag').where('uid', '=', uid).count()


def delete(uid: str):
    for e in _odm.find('flag').where('uid', '=', uid).get():
        e.delete()
