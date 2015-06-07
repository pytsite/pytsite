"""Content Plugin.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import lang, router, assetman
from pytsite.admin import sidebar
from pytsite.taxonomy import taxonomy_manager
from .models import SectionModel

# Dependencies
__import__('pytsite.auth')
__import__('pytsite.admin')
__import__('pytsite.image')
__import__('pytsite.route_alias')
__import__('pytsite.tag')


lang.register_package(__name__)
assetman.register_package(__name__)

router.add_rule('/pytsite/content/view/<string:model>/<string:eid>', 'pytsite.content.eps.view', methods=['GET'])

taxonomy_manager.register_model('section', SectionModel)

sidebar.add_section('content', lang.t(__name__ + '@content'), 100, ('*',))
