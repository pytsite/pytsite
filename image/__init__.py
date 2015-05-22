"""Image plugin init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core import odm, router
from .models import Image

odm.odm_manager.register_model('image', Image)

router.add_rule(
    '/image/resize/<int:width>/<int:height>/<string(length=2):p1>/<string(length=2):p2>/<string:filename>',
    'pytsite.image.endpoints.get_resize'
)
