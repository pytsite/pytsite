"""Content Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import lang
from pytsite.admin import sidebar

# Dependencies
__import__('pytsite.auth')
__import__('pytsite.admin')
__import__('pytsite.image')
__import__('pytsite.route_path')
__import__('pytsite.tag')


lang.register_package(__name__)

sidebar.add_section('content', lang.t(__name__ + '@content'), 100, ('*',))
