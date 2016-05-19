"""Flag Package Event Handlers.
"""
from pytsite import odm as _odm
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def pytsite_odm_entity_delete(entity: _odm=_odm.Entity):
    """Delete all related flags on entity deletion.
    """
    _api.delete(entity)
