"""PytSite ODM Auth API Functions
"""
from typing import Union as _Union
from bson.objectid import ObjectId as _ObjectId
from pytsite import auth as _auth, odm as _odm, permissions as _permissions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def check_permission(perm_type: str, model: str, entity_id: _Union[_ObjectId, str, None] = None,
                     user: _auth.model.AbstractUser = None) -> bool:
    """Check current user's permissions to operate with entity(es).
    """
    global_perm_name = 'pytsite.odm_auth.{}.{}'.format(perm_type, model)
    personal_perm_name = 'pytsite.odm_auth.{}_own.{}'.format(perm_type, model)

    # Get current user
    if not user:
        user = _auth.get_current_user()

    # Check if the user has global permission
    if _permissions.is_permission_defined(global_perm_name) and user.has_permission(global_perm_name):
        return True

    # Check user's personal permission for particular entity
    if entity_id and _permissions.is_permission_defined(personal_perm_name) and user.has_permission(personal_perm_name):
        # Load entity
        entity = _odm.dispense(model, entity_id)

        # Nobody can do anything with non-existent entities
        if not entity:
            return False

        # Check author of the entity
        for author_field in 'author', 'owner':
            if entity.has_field(author_field) and entity.f_get(author_field) == user:
                return True

    return False
