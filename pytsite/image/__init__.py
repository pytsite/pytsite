"""PytSite Image Package.
"""
# Public API
from . import _model as model, _widget as widget
from ._api import create, get, get_by_ref, get_resize_limit_height, get_resize_limit_width, get_resize_step

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import odm, router, assetman

    odm.register_model('image', model.Image)

    router.add_rule(
        '/image/resize/<int:width>/<int:height>/<string(length=2):p1>/<string(length=2):p2>/<string:filename>',
        'pytsite.image@resize'
    )

    assetman.register_package(__name__)


_init()
