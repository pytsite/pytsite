"""PytSite Distributed Lock Manager Lock Object
"""
from typing import Mapping as _Mapping
from os import getpid as _getpid
from time import sleep as _sleep, time as _time
from pytsite import cache as _cache, threading as _threading, router as _router
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_CACHE_POOL = _cache.create_pool('pytsite.dlm')


class Lock:
    def __init__(self, key: str, wait: int = 5, ttl: int = 60):
        """Init
        """
        self._key = key
        self._wait = wait
        self._ttl = ttl

    @staticmethod
    def _get_process_uid() -> str:
        """Get unique thread ID including host name and process number
        """
        return '{}.{}.{}'.format(_router.server_name(), _getpid(), _threading.get_id())

    @property
    def locked(self) -> bool:
        return _CACHE_POOL.has(self._key)

    @property
    def _lock_object(self) -> _Mapping:
        return _CACHE_POOL.get_hash(self._key)

    @_lock_object.setter
    def _lock_object(self, value: _Mapping):
        _CACHE_POOL.put_hash(self._key, value, self._ttl)

    @property
    def _uid(self) -> int:
        try:
            return _CACHE_POOL.get_hash_item(self._key, 'uid')
        except _cache.error.KeyNotExist:
            raise _error.LockNotAcquired(self._key)

    @_uid.setter
    def _uid(self, value: int):
        try:
            _CACHE_POOL.put_hash_item(self._key, 'uid', value)
        except _cache.error.KeyNotExist:
            raise _error.LockNotAcquired(self._key)

    @property
    def _depth(self) -> int:
        try:
            return _CACHE_POOL.get_hash_item(self._key, 'depth')
        except _cache.error.KeyNotExist:
            raise _error.LockNotAcquired(self._key)

    @_depth.setter
    def _depth(self, value: int):
        try:
            _CACHE_POOL.put_hash_item(self._key, 'depth', value)
        except _cache.error.KeyNotExist:
            raise _error.LockNotAcquired(self._key)

    def acquire(self):
        """Acquire lock
        """
        # Prevent other threads to intrude into process of acquiring
        with _threading.get_shared_r_lock():
            # If lock is acquired by current thread
            if self.locked and self._uid == self._get_process_uid():
                self._depth += 1
                return

            # If lock is not acquired by current thread
            else:
                # Wait while lock will be released
                waiting_start = _time()
                while _CACHE_POOL.has(self._key):
                    if _time() - waiting_start > self._wait:
                        raise _error.ReleaseWaitingTimeExceeded(self._key, self._wait)

                    _sleep(0.1)

                # Lock is released, now it is possible to acquire it
                self._lock_object = {'uid': self._get_process_uid(), 'depth': 1}

        return self

    def release(self):
        """Release lock
        """
        # Prevent other threads to intrude into process of releasing
        with _threading.get_shared_r_lock():
            # Check if lock is locked
            if not self.locked:
                raise _error.LockNotAcquired(self._key)

            # Lock can be released only by its creator
            if self._uid != self._get_process_uid():
                raise _error.UnexpectedLockRelease(self._key)

            if self._depth == 1:
                # Remove lock from the storage
                _CACHE_POOL.rm(self._key)
            else:
                # Decrease depth
                self._depth -= 1

    def __enter__(self):
        return self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
