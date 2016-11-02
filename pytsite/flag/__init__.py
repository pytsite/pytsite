"""PytSite Flag Package.
"""
# Public API
from . import _widget as widget
from ._api import flag, average, count, delete, is_flagged, sum, toggle, unflag

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, odm, tpl, lang, events, http_api, permissions
    from . import _model, _eh

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)

    # Permission group
    permissions.define_group('flag', 'pytsite.flag@flag')

    # ODM models
    odm.register_model('flag', _model.Flag)

    # HTTP API aliases
    http_api.register_handler('flag', 'pytsite.flag.http_api')

    # Event listeners
    events.listen('pytsite.setup', _eh.setup)
    events.listen('pytsite.odm.entity.delete', _eh.odm_entity_delete)


_init()
