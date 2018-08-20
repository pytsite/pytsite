"""PytSite Logger
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging as _logging

from os import path as _path, makedirs as _makedirs
from datetime import datetime as _datetime
from pytsite import reg as _reg, cleanup as _cleanup

_log_dir = _reg.get('paths.log')
_log_path = _path.join(_log_dir, _datetime.now().strftime('{}-%Y%m%d.log'.format(_reg.get('env.type'))))
_log_level = _logging.DEBUG if _reg.get('debug') else _logging.INFO

if not _path.exists(_log_dir):
    _makedirs(_log_dir, 0o755, True)

# Create logger
_logger = _logging.getLogger(_reg.get('env.name', 'default'))
_logger.setLevel(_log_level)

# Setup handler
_handler = _logging.FileHandler(_log_path, encoding='utf-8')
if _log_level == _logging.DEBUG:
    fmt = '%(asctime)s %(levelname)7s %(process)d:%(thread)d %(message)s'
else:
    fmt = '%(asctime)s %(levelname)7s %(message)s'
_handler.setFormatter(_logging.Formatter(fmt))
_handler.setLevel(_log_level)
_logger.addHandler(_handler)

# Events handlers
from . import _eh
_cleanup.on_cleanup(_eh.cleanup)

# Public API
from ._api import debug, info, warn, error
