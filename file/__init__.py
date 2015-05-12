"""File.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from ..core import odm
from .models import File

odm.manager.register_model('file', File)