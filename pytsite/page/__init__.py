"""Page Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import content
    from ._model import Page
    content.register_model('page', Page, __name__ + '@pages')

__init()

# Public API
from . import _model as model
from ._functions import replace_model
