"""PytSite ODM Permissions Models.
"""
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class PermMixin:
    def perm_check(self, perm_type: str) -> bool:
        if hasattr(self, 'model') and hasattr(self, 'id'):
            return _api.check_permissions(perm_type, self.model, self.id)
        else:
            raise RuntimeError('Improper usage of this mixin.')
