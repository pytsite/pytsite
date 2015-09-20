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
    from pytsite import console, events, lang
    from . import _command

    def app_update_event():
        """'app.update' event handler.
        """
        console.run_command('odm:reindex')

    lang.register_package(__name__)
    console.register_command(_command.RebuildIndices())
    events.listen('pytsite.update.after', app_update_event)


_init()
