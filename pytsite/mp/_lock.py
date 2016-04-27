"""PytSite Multiprocessing Locks.
"""
import time as _time
from typing import Union as _Union
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from os import getpid as _getpid
from pytsite import cache as _cache, reg as _reg, logger as _logger, threading as _threading

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_REDIS_POOL_NAME = 'pytsite.mp.locks'
_dbg = _reg.get('mp.debug')


def _get_ptid():
    """Get unique ID for current process/thread pair.
    """
    return '{}:{}'.format(_getpid(), _threading.get_id())


class Abstract(_ABC):
    """Abstract Lock.
    """
    def __init__(self, name: str = None, recursive: bool = False):
        """Init.
        """
        self._name = name
        self._recursive = recursive
        self._depth = 0

    @_abstractmethod
    def _get_lock_object(self) -> _Union[dict, None]:
        pass

    @_abstractmethod
    def _create_lock_object(self, ttl: int = None) -> dict:
        """Physically create block.
        """
        pass

    @_abstractmethod
    def _delete_lock_object(self):
        """Physically delete block.
        """
        pass

    def _get_retry_time(self) -> float:
        """Get retry time for waiting loop.
        """
        return 0.1

    def locked(self) -> bool:
        """Check if the lock is locked.
        """
        return bool(self._get_lock_object())

    def lock(self, ttl: int = None):
        """Lock the lock.
        """
        lock_obj = self._get_lock_object()

        # Block does not exist, create it
        if not lock_obj:
            lock_obj = self._create_lock_object(ttl)
            self._depth = 1

        # If already blocked
        else:
            # If this is recursive lock and it has been locked by this process, just increase depth
            if self._recursive and lock_obj['uid'] == _get_ptid():
                self._depth += 1

            # If this lock has been locked by another process, wait while it will be unlocked
            else:
                while True:
                    # Waiting for unlock
                    if _dbg:
                        _logger.debug('Lock WAIT: {}. Recursive: {}, depth: {}, UID: {}'.
                                      format(self._name, self._recursive, self._depth, lock_obj['uid']), __name__)
                    _time.sleep(self._get_retry_time())

                    # Checking if lock has been unlocked
                    if not self._get_lock_object():
                        self._create_lock_object(ttl)
                        self._depth = 1
                        break

        if _dbg:
            _logger.debug("Lock ACQUIRED: {}. Recursive: {}, depth: {}, TTL: {}, UID: {}".
                          format(self._name, self._recursive, self._depth, ttl, lock_obj['uid']), __name__)

    def unlock(self):
        # Do unblocking only if block exists
        lock_object = self._get_lock_object()
        if not lock_object:
            return

        # If the block belongs to current process, decrease depth
        if lock_object['uid'] == _get_ptid():
            self._depth -= 1

        # If depth if 0, we can delete block
        if self._depth == 0:
            self._delete_lock_object()

        if _dbg:
            _logger.debug("Lock RELEASED: {}. Recursive: {}, depth: {}, UID: {}".
                          format(self._name, self._recursive, self._depth, lock_object['uid']), __name__)

    def __enter__(self):
        self.lock()

        return self

    def __exit__(self):
        self.unlock()


class CacheBased(Abstract):
    def __init__(self, name: str = None, recursive: bool = False):
        super().__init__(name, recursive)

        pool_name = 'pytsite.mp.lock'
        if _cache.has_pool(pool_name):
            self._pool = _cache.get_pool(pool_name)
        else:
            self._pool = _cache.create_pool(pool_name, self._get_pool_driver())

    @_abstractmethod
    def _get_pool_driver(self) -> str:
        pass

    def _get_lock_object(self) -> _Union[dict, None]:
        try:
            return self._pool.get(self._name)
        except _cache.error.KeyNotExist:
            return None

    def _create_lock_object(self, ttl: int = None) -> dict:
        return self._pool.put(self._name, {'uid': _get_ptid()}, ttl)

    def _delete_lock_object(self):
        self._pool.rm(self._name)


class Redis(CacheBased):
    def _get_pool_driver(self) -> str:
        return 'redis'
