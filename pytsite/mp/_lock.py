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


_dbg = _reg.get('mp.debug')


def _get_ptid():
    """Get unique ID for current process/thread pair.
    """
    return '{}:{}'.format(_getpid(), _threading.get_id())


class Abstract(_ABC):
    """Abstract Lock.
    """

    def __init__(self, name: str = None, re_entrant: bool = False):
        """Init.
        """
        self._name = name
        self._re_entrant = re_entrant

    @_abstractmethod
    def _get_lock_object(self) -> _Union[dict, None]:
        """Return existing lock object from storage or None if it doesn't exist.
        """
        pass

    @_abstractmethod
    def _create_lock_object(self, ptid: str) -> dict:
        """Create new lock object in a storage.
        """
        pass

    @_abstractmethod
    def _update_lock_object(self, object: dict):
        """Update existing lock object in a storage.
        """
        pass

    @_abstractmethod
    def _delete_lock_object(self):
        """Delete lock object from a storage.
        """
        pass

    def _get_retry_time(self) -> float:
        """Get retry time for waiting loop.
        """
        return 1

    def locked(self) -> bool:
        """Check if the lock is locked.
        """
        return bool(self._get_lock_object())

    def lock(self):
        """Lock the lock.
        """
        # Get lock object from a storage
        lock_obj = self._get_lock_object()

        # Lock object does not exist in storage, create it
        if not lock_obj:
            lock_obj = self._create_lock_object(_get_ptid())
            if _dbg:
                _logger.debug("Lock ACQUIRED: {}. Re-entrant: {}, depth: {}.".
                              format(self._name, self._re_entrant, lock_obj['depth']))

        # If lock object exist in storage
        else:
            if self._re_entrant:
                # If the lock is owned by current process/thread, just increase depth
                if lock_obj['ptid'] == _get_ptid():
                    lock_obj['depth'] += 1
                    self._update_lock_object(lock_obj)
                    if _dbg:
                        _logger.debug("Lock DEPTH INCREASED: {}. Re-entrant: {}, depth: {}.".
                                      format(self._name, self._re_entrant, lock_obj['depth']))
                else:
                    # If the lock is owned by another process/thread, wait while it will be unlocked
                    while True:
                        if _dbg:
                            msg = 'Lock WAIT: {}. Re-entrant: {}, owned by: {}'. \
                                format(self._name, self._re_entrant, lock_obj['ptid'])
                            _logger.debug(msg)

                        # Waiting for unlock
                        _time.sleep(self._get_retry_time())

                        # Check if a lock object was removed from a storage, and re-create it
                        _logger.debug(self.locked())
                        if not self.locked():
                            self.lock()
                            return

            # Lock is not re-entrant so it cannot be locked again
            else:
                raise RuntimeError("Non re-entrant lock {} owned by {} cannot be locked again.".
                                   format(self._name, lock_obj['ptid']))

    def unlock(self):
        """Release the lock.
        """
        lock_obj = self._get_lock_object()

        # Lock storage doesn't have lock object, so lock is not locked
        if not lock_obj:
            return

        if self._re_entrant:
            # Re-entrant lock belongs to the current process and thread
            if lock_obj['ptid'] == _get_ptid():
                # Decrease locking depth
                lock_obj['depth'] -= 1

                # If depth is 0 we must delete lock object
                if lock_obj['depth'] == 0:
                    self._delete_lock_object()
                    msg = "Lock RELEASED: {}. Re-entrant: {}, depth: {}, was owned by: {}". \
                        format(self._name, self._re_entrant, lock_obj['depth'], lock_obj['ptid'])
                    _logger.debug(msg)

                # Depth is not zero yet, just update lock object in the storage
                else:
                    self._update_lock_object(lock_obj)
                    if _dbg:
                        msg = "Lock DEPTH DECREASED: {}. Re-entrant: {}, depth: {}, owned by: {}". \
                            format(self._name, self._re_entrant, lock_obj['depth'], lock_obj['ptid'])
                        _logger.debug(msg)

            # Re-entrant lock cannot be unlocked by another process/thread
            else:
                raise RuntimeError("Current process/thread doesn't own re-entrant lock {}, owned by {}.".
                                   format(self._name, lock_obj['ptid']))

        else:
            self._delete_lock_object()
            if _dbg:
                msg = "Lock RELEASED: {}. Re-entrant: {}, was owned by: {}". \
                    format(self._name, self._re_entrant, lock_obj['ptid'])
                _logger.debug(msg)

    def __enter__(self):
        self.lock()

        return self

    def __exit__(self):
        self.unlock()


class CacheBased(Abstract):
    def __init__(self, name: str = None, re_entrant: bool = False):
        """Init.
        """
        super().__init__(name, re_entrant)

        pool_name = 'pytsite.mp.lock'

        # Get existing or create new cache pool to store lock objects
        if _cache.has_pool(pool_name):
            self._pool = _cache.get_pool(pool_name)
        else:
            # Create new pool and clear ALL its previous data
            self._pool = _cache.create_pool(pool_name, self._get_pool_driver_name())
            self._pool.clear()

    @_abstractmethod
    def _get_pool_driver_name(self) -> str:
        """Get cache's driver name.
        """
        pass

    def _get_lock_object(self) -> _Union[dict, None]:
        try:
            return self._pool.get(self._name)
        except _cache.error.KeyNotExist:
            return None

    def _create_lock_object(self, ptid: str) -> dict:
        """Create new lock object in the storage.
        """
        if not ptid:
            raise RuntimeError('Process/thread ID cannot be empty.')

        return self._pool.put(self._name, {'ptid': ptid, 'depth': 1})

    def _update_lock_object(self, obj: dict):
        """Update existing lock object in a storage.
        """
        self._pool.put(self._name, obj)

    def _delete_lock_object(self):
        """Delete lock object from the storage.
        """
        self._pool.rm(self._name)
