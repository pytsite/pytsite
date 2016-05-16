"""PytSite Block Package.
"""
from pytsite import content as _content

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from . import _model
    _content.register_model('block', _model.Block, 'pytsite.block@blocks', 1000, 'fa fa-th')


_init()
