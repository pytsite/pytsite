"""Object Document Mapper Package Init
"""
# Public API
from . import _field as field, _validation as validation, _error as error, _geo as geo
from ._entity import Entity, I_ASC, I_DESC, I_TEXT, I_GEO2D, I_GEOSPHERE
from ._finder import Finder, Result as FinderResult
from ._api import register_model, unregister_model, is_model_registered, get_model_class, get_registered_models, \
    resolve_ref, get_by_ref, dispense, find, aggregate

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import console, lang, events
    from . import _console_command, _eh

    # Resources
    lang.register_package(__name__)

    # Console commands
    console.register_command(_console_command.ODM())

    # Reindex collections on every update
    events.listen('pytsite.update.after', _eh.pytsite_update_after)

__init()
