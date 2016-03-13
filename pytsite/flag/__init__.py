"""PytSite Flag Package.
"""
# Public API
from . import _widget as widget
from ._api import count, delete

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import assetman, odm, tpl, lang, events, ajax
    from . import _model, _eh

    odm.register_model('flag', _model.Flag)
    lang.register_package(__name__)
    tpl.register_package(__name__)

    assetman.register_package(__name__)
    assetman.add('pytsite.flag@js/common.js', permanent=True)

    events.listen('pytsite.odm.entity.delete', _eh.odm_entity_delete)

    ajax.register_ep('pytsite.flag.ep.toggle')

__init()
