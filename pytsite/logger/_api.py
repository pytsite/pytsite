"""PytSite Logger API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging
from pytsite import reg

logger = logging.getLogger(reg.get('env.name', 'default'))


def _log(level: int, msg, *args, **kwargs):
    if isinstance(msg, Exception):
        kwargs['exc_info'] = msg

    logger.log(level, msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    _log(logging.DEBUG, msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    _log(logging.INFO, msg, *args, **kwargs)


def warn(msg, *args, **kwargs):
    _log(logging.WARNING, msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    _log(logging.ERROR, msg, *args, **kwargs)
