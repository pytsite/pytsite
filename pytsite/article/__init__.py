"""Article Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import reg
from pytsite.content import content_manager
from .models import ArticleModel


content_manager.register_model('article', reg.get('article.model', ArticleModel))
