"""Tag Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import lang
from pytsite.taxonomy import _manager
from .models import Tag

lang.register_package(__name__)

_manager.register_model('tag', Tag, __name__ + '@tags')
