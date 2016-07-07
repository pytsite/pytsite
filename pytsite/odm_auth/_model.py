"""PytSite ODM Permissions Models.
"""
from pytsite import odm as _odm, auth as _auth
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class PermissableEntity(_odm.model.Entity):
    """Entity which has owner and can be authorized to perform certain actions on it.
    """

    def check_perm(self, action: str) -> bool:
        """Check current user's permissions.
        """
        return _api.check_permissions(action, self.model, self.id)

    def _pre_save(self):
        super()._pre_save()

        # If entity's owner was deleted, set it to first administrator
        for f_name in 'author', 'owner':
            if self.has_field(f_name) and not self.f_get(f_name):
                c_user = _auth.current_user()
                if not c_user.is_anonymous:
                    if self.is_new and c_user.has_permission('pytsite.odm_perm.create.' + self.model):
                        # Entity is new and user has permission to create it
                        self.f_set(f_name, c_user)
                    elif not self.is_new and c_user.has_permission('pytsite.odm_perm.modify.' + self.model):
                        # Entity is not new and user has permission to modify any entity of this model
                        self.f_set(f_name, c_user)
                    else:
                        # User does not have necessary permissions, make first admin as author
                        self.f_set(f_name, _auth.first_admin_user())
                else:
                    # Current user is anonymous, make first admin as author
                    self.f_set(f_name, _auth.first_admin_user())
