"""PytSite Logger.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import logging as __logging

__logger = __logging.getLogger(__name__)


def info(msg: str, *args, **kwargs):
    global __logger
    __logger.info(msg, *args, **kwargs)