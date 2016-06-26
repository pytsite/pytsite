"""PytSite ODM Permissions Package.
"""
# Public API
from . import _model as model
from ._api import check_permissions, disable_perm_check, enable_perm_check, is_perm_check_enabled

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import events
    from . import _eh

    # Event listeners
    events.listen('pytsite.odm.register_model', _eh.odm_register_model)
    events.listen('pytsite.odm.entity.pre_save', _eh.odm_entity_pre_save)
    events.listen('pytsite.odm.entity.pre_delete', _eh.odm_entity_pre_delete)


_init()