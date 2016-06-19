"""PytSite ODM Permissions Models.
"""
from pytsite import odm as _odm
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AuthorizableEntity(_odm.model.Entity):
    """Entity which has owner and can be authorized to perform certain actions on it.
    """

    def perm_check(self, action: str) -> bool:
        return _api.check_permissions(action, self.model, self.id)
