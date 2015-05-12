"""Image plugin init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from ..core import odm, router
from .models import Image

odm.manager.register_model('image', Image)

router.add_rule('/image/resize/<width>/<height>/<id>', 'pytsite.image.views.get_resize')