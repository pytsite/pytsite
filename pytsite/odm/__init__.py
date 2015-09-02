"""Object Document Mapper Package Init
"""
# Public API
from . import _field as field, _validation as validation, _error as error
from ._model import Model, I_ASC, I_DESC, I_TEXT, I_GEO2D
from ._finder import Finder, Result as FinderResult
from ._functions import register_model, find, dispense, get_by_ref, resolve_ref

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _app_update_event():
    """'app.update' event handler.
    """
    from pytsite import console
    console.run_command('odm:reindex')


def __init():
    from pytsite import console
    from pytsite import events
    from pytsite import lang
    from . import _command

    lang.register_package(__name__)
    console.register_command(_command.RebuildIndices())
    events.listen('pytsite.update.after', _app_update_event)


__init()
