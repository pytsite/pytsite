"""PytSite ODM Auth API Functions
"""
from typing import Optional as _Optional
from pytsite import auth as _auth, odm as _odm, permissions as _permissions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def check_permission(perm: str, model: str, ids: _Optional[str, list, tuple] = None,
                     user: _auth.model.AbstractUser = None) -> bool:
    """Check current user's permissions to operate with entity(es).
    """
    full_perm = 'pytsite.odm_auth.{}.{}'.format(perm, model)

    # Get current user
    if not user:
        user = _auth.get_current_user()

    # Check for permission existence
    if not _permissions.is_permission_defined(full_perm):
        return False

    if isinstance(ids, str):
        ids = (ids,)

    # Check user's personal permission
    if perm.endswith('_own'):
        if ids is None:
            raise RuntimeError('Entity IDs must be provided')

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

                    if not isinstance(author, _auth.model.AbstractUser) and author is not None:
                        raise RuntimeError('Entity must return user object or None here')

                    if author != user:
                        return False

    # Check global permission
    elif user.has_permission(full_perm):
        return True

    return False
