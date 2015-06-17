"""Article Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import content
    from pytsite.core import reg
    from ._model import ArticleModel
    content.manager.register_model('article', reg.get('article.model', ArticleModel), __name__ + '@products')

__init()

# Public API
from . import _model as model
