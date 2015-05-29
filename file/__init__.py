"""File.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__import__('pytsite.auth')
__import__('pytsite.jquery_ui')

from pytsite.core.odm import odm_manager
from pytsite.core import assetman, router, lang, tpl
from .models import File

odm_manager.register_model('file', File)

assetman.register_package(__name__)

router.add_rule('/pytsite/file/upload/<string:model>',
                'pytsite.file.eps.post_upload',
                filters=('pytsite.auth.eps.filter_authorize',),
                methods=['POST'])

lang.register_package(__name__)

tpl.register_package(__name__)
