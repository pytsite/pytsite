"""PytSite Distributed Lock Manager API
"""
from ._lock import Lock as _Lock

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def lock(key: str, ttl: int = 60) -> _Lock:
    """Create a lock object
    """
    return _Lock(key, ttl)
