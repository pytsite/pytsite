"""PytSite Distributed Lock Manager Errors
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class UnexpectedLockRelease(Exception):
    def __init__(self, key: str):
        super().__init__()
        self._key = key

    def __str__(self):
        return "Distributed lock '{}' was unexpectedly released".format(self._key)


class UnexpectedLockOverwrite(Exception):
    def __init__(self, key: str):
        super().__init__()
        self._key = key

    def __str__(self):
        return "Distributed lock '{}' was unexpectedly overwritten".format(self._key)


class ReleaseWaitingTimeExceeded(Exception):
    def __init__(self, key: str, seconds: int):
        super().__init__()
        self._key = key
        self._seconds = seconds

    def __str__(self):
        return "Waiting time for distributed lock '{}' exceeded {} seconds".format(self._key, self._seconds)


class LockNotAcquired(Exception):
    def __init__(self, key: str):
        super().__init__()
        self._key = key

    def __str__(self):
        return "Distributed lock '{}' is not acquired".format(self._key)
