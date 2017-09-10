"""Object Document Mapper Package Init
"""
from pytsite import cache as _cache, reg as _reg
_cache.create_pool('pytsite.odm.entities', _reg.get('odm.cache.driver', 'redis'))

# Public API
from . import _field as field, _validation as validation, _error as error, _geo as geo, _model as model
from ._model import I_ASC, I_DESC, I_TEXT, I_GEO2D, I_GEOSPHERE
from ._finder import Finder, Result as FinderResult
from ._api import register_model, unregister_model, is_model_registered, get_model_class, get_registered_models, \
    resolve_ref, resolve_refs, get_by_ref, dispense, find, aggregate, get_finder_cache

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import console, lang, events, update
    from . import _console_command, _eh

    # Resources
    lang.register_package(__name__)

    # Console commands
    console.register_command(_console_command.Reindex())

    # Event listeners
    update.on_update_after(_eh.update_after, 999)  # Low priority to wait while plugman finish upgrade
    events.listen('pytsite.db.restore', _eh.db_restore)


_init()
