"""Object Document Mapper Package Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _app_update_event():
    """'app.update' event handler.
    """
    from pytsite.core import console
    console.run_command('odm:reindex')


def __init():
    from pytsite.core import lang, console, events
    from . import _console_commands

    lang.register_package(__name__)
    console.register_command(_console_commands.RebuildIndices())
    events.listen('app.update', _app_update_event)

__init()


# Public API
from pymongo import ASCENDING as I_ASC, DESCENDING as I_DESC, GEO2D as I_GEO2D
from . import _field as field, _validation as validation, _error as error
from ._model import Model
from ._finder import Finder, Result as FinderResult
from ._functions import register_model, find, dispense, get_by_ref, resolve_ref
