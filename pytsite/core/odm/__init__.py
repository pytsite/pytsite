"""Object Document Mapper Package Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pymongo as _pymongo
from . import _model, _field, _manager, _finder, _validation, _error


def _app_update_event():
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
I_ASC = _pymongo.ASCENDING
I_DESC = _pymongo.DESCENDING
I_GEO2D = _pymongo.GEO2D
Model = _model.Model
Finder = _finder.Finder
field = _field
validation = _validation
error = _error
register_model = _manager.register_model
find = _manager.find
dispense = _manager.dispense
get_by_ref = _manager.get_by_ref
resolve_ref = _manager.resolve_ref
