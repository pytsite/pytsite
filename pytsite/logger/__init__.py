"""PytSite Logger
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging as _logging
from typing import Union as _Union
from os import path as _path, makedirs as _makedirs
from datetime import datetime as _datetime
from pytsite import reg as _reg

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
_handler.setLevel(_log_level)
_logger.addHandler(_handler)

# Setup formatter
# https://docs.python.org/3/library/logging.html#logrecord-attributes
_handler.setFormatter(_logging.Formatter('%(asctime)s %(levelname)7s %(process)d:%(thread)d %(message)s'))


def _log(level: int, msg: _Union[str, Exception], **kwargs):
    if isinstance(msg, Exception):
        kwargs['exc_info'] = msg

    _logger.log(level, msg, **kwargs)


def debug(msg: _Union[str, Exception], **kwargs):
    _log(_logging.DEBUG, msg, **kwargs)


def info(msg: _Union[str, Exception], **kwargs):
    _log(_logging.INFO, msg, **kwargs)


def warn(msg: _Union[str, Exception], **kwargs):
    _log(_logging.WARNING, msg, **kwargs)


def error(msg: _Union[str, Exception], **kwargs):
    _log(_logging.ERROR, msg, **kwargs)
