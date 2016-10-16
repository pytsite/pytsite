"""PytSite ODM File Storage.
"""
from . import _model as model, _field as field
from ._driver import Driver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import odm, events, router
    from . import _model, _eh

    # Register ODM models
    odm.register_model('file', _model.AnyFileODMEntity)
    odm.register_model('file_image', _model.ImageFileODMEntity)

    # Event handlers
    events.listen('pytsite.update', _eh.update)

    router.add_rule(
        '/image/resize/<int:width>/<int:height>/<string(length=2):p1>/<string(length=2):p2>/<string:filename>',
        'pytsite.file_storage_odm@image',
    )


_init()
