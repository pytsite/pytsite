"""Image plugin init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import odm
    from pytsite import router
    from ._model import Image

    odm.register_model('image', Image)

    router.add_rule(
        '/image/resize/<int:width>/<int:height>/<string(length=2):p1>/<string(length=2):p2>/<string:filename>',
        'pytsite.image.eps.get_resize'
    )


__init()


# Public API
from . import _model as model, _widget as widget
from ._functions import create
