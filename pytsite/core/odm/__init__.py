"""Object Document Mapper Package Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pymongo as _pymongo
from . import _model, _field, _manager, _finder, _validation, _error

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
