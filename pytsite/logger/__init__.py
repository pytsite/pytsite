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

if not _path.exists(_log_dir):
    _makedirs(_log_dir, 0o755, True)

# Define logger format
# https://docs.python.org/3/library/logging.html#logrecord-attributes
if _dbg:
    _format = '%(asctime)s %(levelname)7s %(process)d:%(thread)d %(pathname)s:%(lineno)d %(message)s'
else:
    _format = '%(asctime)s %(levelname)7s %(process)d:%(thread)d %(message)s'

_log_stream = open(_log_path, 'at', encoding='utf-8', errors='replace')
_logging.basicConfig(stream=_log_stream, format=_format)
_logger = _logging.getLogger(_reg.get('env.name', 'default'))
_level = _logging.DEBUG if _reg.get('debug') else _logging.INFO
_logger.setLevel(_level)

# Public API
debug = _logger.debug
info = _logger.info
warn = _logger.warn
error = _logger.error
