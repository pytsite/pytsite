"""Object Document Mapper Package Init
"""
# Public API
from . import _field as field, _validation as validation, _error as error
from ._model import Model, I_ASC, I_DESC, I_TEXT, I_GEO2D
from ._finder import Finder, Result as FinderResult
from ._functions import register_model, find, dispense, get_by_ref, resolve_ref, get_registered_models, \
    is_model_registered, get_model_class

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import console, lang
    from . import _command

    lang.register_package(__name__)
    console.register_command(_command.RebuildIndices())


_init()
