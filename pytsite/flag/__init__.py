"""PytSite Flag Package.
"""
# Public API
from . import _widget as widget
from ._api import count, delete

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    import sys
    from pytsite import assetman, odm, tpl, lang, events
    from . import _model, _eh

    lang.register_package(__name__)

    tpl.register_package(__name__)
    tpl.register_global('flag', sys.modules[__package__])

    odm.register_model('flag', _model.Flag)

    assetman.register_package(__name__)
    assetman.add('pytsite.flag@css/common.css', forever=True)
    assetman.add('pytsite.flag@js/common.js', forever=True)

    events.listen('pytsite.odm.entity.delete', _eh.odm_entity_delete)

__init()
