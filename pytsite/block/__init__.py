"""PytSite Block Package.
"""
from . import _error as error
from ._api import get_block

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import content, tpl
    from . import _model, _api

    # Content model
    content.register_model('block', _model.Block, 'pytsite.block@blocks', 1000, 'fa fa-th')

    # Tpl global callback
    def tpl_global_render_block(uid) -> str:
        try:
            return get_block(uid).body
        except error.BlockNotFound:
            return ''

    # Tpl globals
    tpl.register_global('block_render', tpl_global_render_block)

_init()
