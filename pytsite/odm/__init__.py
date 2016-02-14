"""Object Document Mapper Package Init
"""
# Public API
from . import _field as field, _validation as validation, _error as error
from ._model import Model, I_ASC, I_DESC, I_TEXT, I_GEO2D
from ._finder import Finder, Result as FinderResult
from ._api import register_model, unregister_model, is_model_registered, get_model_class, get_registered_models, \
    resolve_ref, get_by_ref, dispense, cache_get, cache_put, cache_delete, find

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import console, lang, events
    from . import _console_command, _finder_cache

    # Resources
    lang.register_package(__name__)

    # Console commands
    console.register_command(_console_command.ODM())

    # Run finder cache garbage collector every minute
    events.listen('pytsite.cron.1min', lambda: _finder_cache.collect_garbage())


__init()
