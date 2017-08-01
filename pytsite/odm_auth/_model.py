"""PytSite ODM Authorizable Entity Model
"""
from typing import Tuple as _Tuple
from pytsite import odm as _odm, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AuthorizableEntity(_odm.model.Entity):
    """Entity which has owner and can be authorized to perform certain actions on it.
    """

    @classmethod
    def odm_auth_permissions_group(cls) -> str:
        """Get model permission group name
        """
        return cls.get_package_name().split('.')[-1]

    @classmethod
    def odm_auth_permissions(cls) -> _Tuple[str, ...]:
        """Get permissions supported by model
        """
        return 'create', 'view', 'modify', 'delete', 'view_own', 'modify_own', 'delete_own'

    def odm_auth_check_permission(self, perm: str, user: _auth.model.AbstractUser = None) -> bool:
        """Check user's permissions
        """
        from . import _api
        return _api.check_permission(perm, self.model, self.id, user)

    def f_get(self, field_name: str, **kwargs):
        """Get field's value
        """
        if field_name in ('author', 'owner'):
            try:
                return super().f_get(field_name, **kwargs)

            # Owner was deleted or for some reason cannot be accessed
            except _auth.error.UserNotExist:
                # Set first admin as owner
                self.f_set(field_name, _auth.get_first_admin_user()).save()

                return super().f_get(field_name, **kwargs)
