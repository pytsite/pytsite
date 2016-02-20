"""PytSite Logger.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging as _logging
from os import path as _path, makedirs as _makedirs
from datetime import datetime as _datetime
from pytsite import reg as _reg


_log_dir = _reg.get('paths.log')
_now = _datetime.now()
_log_path = _path.join(_log_dir, _now.strftime('%Y%m%d.log'))

if not _path.exists(_log_dir):
    _makedirs(_log_dir, 0o755, True)

_format = '%(asctime)s %(levelname)s %(message)s'
_logging.basicConfig(filename=_log_path, datefmt='%Y-%m-%d %H:%M:%S', format=_format)
_logger = _logging.getLogger(_reg.get('env.name', 'default'))
_level = _logging.DEBUG if _reg.get('debug') else _logging.INFO
_logger.setLevel(_level)


def debug(msg: str, prefix: str=None):
    """Log a DEBUG message.
    """
    if prefix:
        msg = '{} {}'.format(prefix, msg)

    _logger.debug(msg)


def info(msg: str, prefix: str=None):
    """Log an INFO message.
    """
    if prefix:
        msg = '{} {}'.format(prefix, msg)

    _logger.info(msg)


def warn(msg: str, prefix: str=None):
    """Log a WARNING message.
    """
    if prefix:
        msg = '{} {}'.format(prefix, msg)

    _logger.warn(msg)


def error(msg: str, prefix: str=None, exc_info=True):
    """Log an ERROR message.
    """
    if prefix:
        msg = '{} {}'.format(prefix, msg)

    _logger.error(msg, exc_info=exc_info)
