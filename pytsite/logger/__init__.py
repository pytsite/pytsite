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

_format = '%(asctime)s %(levelname)s %(module_name)s %(message)s'
_logging.basicConfig(filename=_log_path, datefmt='%Y-%m-%d %H:%M:%S', format=_format)
_logger = _logging.getLogger(_reg.get('env.name', 'default'))
_level = _logging.DEBUG if _reg.get('logger.level') == 'debug' else _logging.INFO
_logger.setLevel(_level)


def debug(msg: str, module: str='UNKNOWN'):
    """Log an DEBUG message.
    """
    _logger.debug(msg, extra={'module_name': module})


def info(msg: str, module: str='UNKNOWN'):
    """Log an INFO message.
    """
    _logger.info(msg, extra={'module_name': module})


def error(msg: str, *args, **kwargs):
    """Log an ERROR message.
    """
    if 'extra' not in kwargs:
        kwargs['extra'] = {}

    kwargs['exc_info'] = True
    _logger.error(msg, *args, **kwargs)
