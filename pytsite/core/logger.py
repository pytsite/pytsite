"""PytSite Logger.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging as _logging
from os import path as _path, makedirs as _makedirs
from datetime import datetime as _datetime
from . import reg as _reg


_log_dir = _reg.get('paths.log')
_now = _datetime.now()
_log_path = _path.join(_log_dir, _now.strftime('%Y%m%d.log'))

if not _path.exists(_log_dir):
    _makedirs(_log_dir, 0o755, True)

_format = '%(asctime)s %(name)s %(levelname)-8s "%(message)s"'
_logging.basicConfig(filename=_log_path, datefmt='%Y-%m-%d %H:%M:%S', format=_format)
_logger = _logging.getLogger(_reg.get('env.name', 'default'))
_logger.setLevel(_logging.INFO)


def info(msg: str, *args, **kwargs):
    """Log an info message.
    """
    if 'extra' not in kwargs:
        kwargs['extra'] = {}

    _logger.info(msg, *args, **kwargs)


def error(msg: str, *args, **kwargs):
    """Log an error message.
    """
    if 'extra' not in kwargs:
        kwargs['extra'] = {}

    kwargs['exc_info'] = True
    _logger.error(msg, *args, **kwargs)
