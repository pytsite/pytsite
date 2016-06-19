"""PytSite ODM Permissions Package.
"""
# Public API
from . import _model as model
from ._api import check_permissions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import events, lang
    from . import _eh

    # Resources
    lang.register_package(__name__)

    # Event listeners
    events.listen('pytsite.odm.register_model', _eh.odm_register_model)
    events.listen('pytsite.odm.entity.pre_save', _eh.odm_entity_pre_save)
    events.listen('pytsite.odm.entity.pre_delete', _eh.odm_entity_pre_delete)


_init()
