"""Article Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import content
    from ._model import Article
    content.register_model('article', Article, __name__ + '@articles')

__init()

# Public API
from . import _model as model
from ._functions import replace_model
