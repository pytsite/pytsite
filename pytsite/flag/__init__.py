"""PytSite Flag Package.
"""
# Public API
from . import _widget as widget
from ._api import flag, average, count, delete, is_flagged, sum, toggle, unflag

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import assetman, odm, tpl, lang, events, ajax
    from . import _model, _eh

    # ODM models
    odm.register_model('flag', _model.Flag)

    # Resources
    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)

    events.listen('pytsite.odm.entity.delete', _eh.odm_entity_delete)

    ajax.register_ep('pytsite.flag.ep.toggle')

__init()
