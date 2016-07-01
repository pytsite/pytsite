"""PytSite ODM Permissions API Functions.
"""
from typing import Iterable as _Iterable
from pytsite import permission as _permission, auth as _auth, auth_storage_odm as _auth_storage_odm, odm as _odm, \
    threading as _threading

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Thread safe permission checking disable flag
_disable_perm_check = {}


def is_perm_check_enabled() -> bool:
    return _threading.get_id() not in _disable_perm_check


def disable_perm_check():
    _disable_perm_check[_threading.get_id()] = True


def enable_perm_check():
    tid = _threading.get_id()
    if tid in _disable_perm_check:
        del _disable_perm_check[tid]


def check_permissions(action: str, model: str, ids: _Iterable = None) -> bool:
    """Check current user's permissions to operate with entity(es).
    """
    # Get current user
    current_user = _auth.current_user()  # type: _auth_storage_odm.model.User

    # Check ids type
    if ids and type(ids) not in (list, tuple):
        ids = (ids,)

    if action == 'create':
        create_perm_name = 'pytsite.odm_perm.create.' + model
        if _permission.is_permission_defined(create_perm_name) and current_user.has_permission(create_perm_name):
            return True
    else:
        # If 'global' permission was not defined
        global_perm_name = 'pytsite.odm_perm.' + action + '.' + model
        if not _permission.is_permission_defined(global_perm_name):
            return False

        # If user has 'global' permissions for model
        if current_user.has_permission(global_perm_name):
            return True

        # If 'personal' permission was not defined
        personal_perm_name = 'pytsite.odm_perm.' + action + '_own.' + model
        if not _permission.is_permission_defined(personal_perm_name):
            return False

        # Else check user's personal permission
        if current_user.has_permission(personal_perm_name):
            if ids:
                # Check each entity
                for eid in ids:
                    entity = _odm.dispense(model, eid)

                    # Anyone cannot do anything with non-existent entities
                    if not entity:
                        return False

                    # Searching for author of the entity
                    for author_field in 'author', 'owner':
                        if entity.has_field(author_field):
                            author = entity.f_get(author_field)
                            if isinstance(author, _auth.model.AbstractUser) and author.uid == current_user.uid:
                                return True

                            # Entity belongs to nobody
                            elif author is None:
                                return True
            else:
                return True

    return False
