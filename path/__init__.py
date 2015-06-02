"""Path Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.odm import odm_manager
from .models import Path

odm_manager.register_model('path', Path)
