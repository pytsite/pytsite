"""PytSite Logger.
"""
import logging as _logging
from os import path as _path, makedirs as _makedirs
from datetime import datetime as _datetime
from pytsite import reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_dbg = _reg.get('debug', False)
_log_dir = _reg.get('paths.log')
_now = _datetime.now()
_log_path = _path.join(_log_dir, _now.strftime('%Y%m%d.log'))
_log_level = _logging.DEBUG if _reg.get('debug') else _logging.INFO

if not _path.exists(_log_dir):
    _makedirs(_log_dir, 0o755, True)

# Create logger
_logger = _logging.getLogger(_reg.get('env.name', 'default'))
_logger.setLevel(_log_level)

# Setup handler
_handler = _logging.FileHandler(_log_path, encoding='utf-8')
_handler.setLevel(_log_level)
_logger.addHandler(_handler)

# Setup formatter
# https://docs.python.org/3/library/logging.html#logrecord-attributes
if _dbg:
    _format = '%(asctime)s %(levelname)7s %(process)d:%(thread)d %(pathname)s:%(lineno)d %(message)s'
else:
    _format = '%(asctime)s %(levelname)7s %(process)d:%(thread)d %(message)s'
_handler.setFormatter(_logging.Formatter(_format))

# Public API
debug = _logger.debug
info = _logger.info
warn = _logger.warn
error = _logger.error
