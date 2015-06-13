"""Tag Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import lang
from pytsite.taxonomy import taxonomy_manager
from .models import Tag

lang.register_package(__name__)

taxonomy_manager.register_model('tag', Tag)
