"""Article Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import content
    from pytsite.core import reg
    from ._model import Article
    content.register_model('article', reg.get('article.model', Article), __name__ + '@products')

__init()

# Public API
from . import _model as model
