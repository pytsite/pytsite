"""PytSite Logger API Functions
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging as _logging
from pytsite import reg as _reg

_logger = _logging.getLogger(_reg.get('env.name', 'default'))


def _log(level: int, msg, **kwargs):
    if isinstance(msg, Exception):
        kwargs['exc_info'] = msg

    _logger.log(level, msg, **kwargs)


def debug(msg, **kwargs):
    _log(_logging.DEBUG, msg, **kwargs)


def info(msg, **kwargs):
    _log(_logging.INFO, msg, **kwargs)


def warn(msg, **kwargs):
    _log(_logging.WARNING, msg, **kwargs)


def error(msg, **kwargs):
    _log(_logging.ERROR, msg, **kwargs)
