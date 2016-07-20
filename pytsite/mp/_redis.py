"""PytSite Multiprocessing Locks Redis Implementation.
"""
from . import _lock

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Lock(_lock.CacheBased):
    def _get_pool_driver_name(self) -> str:
        """Get cache's driver name.
        """
        return 'redis'
