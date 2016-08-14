"""Flag Package Event Handlers.
"""
from pytsite import odm as _odm, auth as _auth
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def setup():
    """`pytsite.setup` event handler.
    """
    # Allow ordinary users to create, modify and delete images
    user_role = _auth.get_role('user')
    user_role.permissions = list(user_role.permissions) + [
        'pytsite.odm_perm.create.flag',
        'pytsite.odm_perm.delete_own.flag',
    ]
    user_role.save()


def odm_entity_delete(entity: _odm=_odm.model.Entity):
    """'pytsite.odm.entity.delete' event handler.
    """
    # Delete all related flags on entity deletion.
    _api.delete(entity)
