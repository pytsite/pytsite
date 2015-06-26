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


def _init():
    from pytsite.core import lang, console, events
    from . import _console_commands

    lang.register_package(__name__)

    console.register_command(_console_commands.RebuildIndices())

    events.listen('app.update', _app_update_event)

_init()

# Public API
I_ASC = _pymongo.ASCENDING
I_DESC = _pymongo.DESCENDING
I_GEO2D = _pymongo.GEO2D
finder = _finder
model = _model
field = _field
manager = _manager
validation = _validation
error = _error
