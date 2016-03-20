"""PytSite Multiprocessing Locks.
"""
import time as _time
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import cache as _cache, reg as _reg, logger as _logger

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_REDIS_POOL_NAME = 'pytsite.mp.locks'
_dbg = _reg.get('mp.debug')


class Abstract(_ABC):
    def __init__(self, name: str = None, recursive: bool = False):
        self._name = name
        self._recursive = recursive
        self._depth = 0

    @_abstractmethod
    def _is_blocked(self) -> bool:
        pass

    @_abstractmethod
    def _block(self, ttl: int = None):
        pass

    @_abstractmethod
    def _unblock(self):
        pass

    def _get_retry_time(self) -> float:
        return 0.1

    def locked(self) -> bool:
        return self._is_blocked()

    def lock(self, ttl: int = None):
        # If not blocked
        if not self._is_blocked():
            self._block(ttl)

            if self._recursive:
                self._depth += 1

        # If already blocked
        else:
            # If lock has been locked by this process
            if self._recursive and self._depth:
                self._depth += 1

            # If this lock has been locked by another process
            else:
                while True:
                    # Waiting for unlock
                    if _dbg:
                        _logger.debug('Lock WAIT: {}'.format(self._name), __name__)
                    _time.sleep(self._get_retry_time())

                    # Checking if lock has been unlocked
                    if not self._is_blocked():
                        self._block(ttl)

                        if self._recursive:
                            self._depth += 1
        if _dbg:
            _logger.debug("Lock '{}' ACQUIRED. Recursive: {}, depth: {}".
                          format(self._name, self._recursive, self._depth), __name__)

    def unlock(self):
        if self._recursive and self._depth:
            self._depth -= 1

            if not self._depth:
                self._unblock()
        else:
            self._unblock()

        if _dbg:
            _logger.debug("Lock '{}' RELEASED. Recursive: {}, depth: {}".
                          format(self._name, self._recursive, self._depth), __name__)

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

    def _is_blocked(self) -> bool:
        return self._pool.has(self._name)

    def _block(self, ttl: int = None):
        self._pool.put(self._name, True, ttl)

    def _unblock(self):
        self._pool.rm(self._name)


class Db(CacheBased):
    def _get_retry_time(self) -> float:
        return 0.5

    def _get_pool_driver(self) -> str:
        return 'db'


class Redis(CacheBased):
    def _get_pool_driver(self) -> str:
        return 'redis'
