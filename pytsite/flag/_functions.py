"""Flag Package Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import odm as _odm


def count(uid: str) -> int:
    return _odm.find('flag').where('uid', '=', uid).count()
