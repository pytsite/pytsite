"""PytSite Db Cache Driver.
"""
import pickle as _pickle
from typing import Any as _Any, Union as _Union
from datetime import datetime as _datetime, timedelta as _timedelta
from pytsite import reg as _reg, db as _db, logger as _logger
from ._abstract import Abstract as _Abstract

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_dbg = _reg.get('cache.debug')
_collection_name = 'pytsite_cache'


class Db(_Abstract):
    """Database Cache Driver.
    """
    def __init__(self, name: str):
        """Init.
        """
        super().__init__(name)

        self._collection = _db.get_collection('pytsite_cache')

        cols = _db.get_collection_names()
        if _collection_name not in cols or 'name_1' not in self._collection.index_information():
            self._collection.create_index('name', unique=True, background=True)

    def _get_fq_key(self, key: str) -> str:
        """
        """
        return self._name + ':' + key

    def _get_db_item(self, key: str):
        return self._collection.find_one({'$or': [
            {'name': self._get_fq_key(key), 'expires': None},
            {'name': self._get_fq_key(key), 'expires': {'$gt': _datetime.now()}},
        ]})

    def has(self, key: str) -> bool:
        """Check whether an item is in the pool.
        """
        r = bool(self._get_db_item(key))

        if _dbg:
            if r:
                _logger.debug("Pool '{}' HAS '{}'.".format(self.name, key), __name__)
            else:
                _logger.debug("Pool '{}' DOES NOT HAVE '{}'.".format(self.name, key), __name__)

        return r

    def get(self, key: str) -> _Union[_Any, None]:
        """Get an item from the pool.
        """
        item = self._get_db_item(key)

        if item:
            if _reg.get('cache.debug'):
                _logger.debug("GET '{}' from pool '{}'.".format(key, self.name), __name__)

            return _pickle.loads(item['value'])

    def put(self, key: str, value: _Any, ttl: int = None) -> _Any:
        """Put an item into the pool.
        """
        self._collection.update_one({'name': self._get_fq_key(key)}, {
            '$set': {
                'value': _pickle.dumps(value),
                'expires': _datetime.now() + _timedelta(seconds=ttl) if ttl else None,
            }
        }, True)

        if _reg.get('cache.debug'):
            _logger.debug("PUT '{}' into the pool '{}' with TTL {}.".format(key, self.name, ttl), __name__)

        return value

    def rnm(self, key: str, new_key: str):
        """Rename a key.
        """
        item = self._get_db_item(key)
        if not item:
            raise KeyError("Item '{}' does not exist in pool '{}'.".format(key, self._name))

        self.rm(key)
        self.put(new_key, item['value'], item['ttl'])

        if _reg.get('cache.debug'):
            _logger.debug("RENAME '{}' to '{}' in the pool '{}'.".format(key, new_key, self.name), __name__)

    def rm(self, key: str):
        """Remove a single item from the pool.
        """
        self._collection.delete_one({'name': self._get_fq_key(key)})

        if _reg.get('cache.debug'):
            _logger.debug("REMOVE '{}' from the pool '{}'.".format(key, self.name), __name__)

    def clear(self):
        """Clear entire pool.
        """
        self._collection.delete_many({'name': {'$regex': '^{}:'.format(self._name)}})

        if _reg.get('cache.debug'):
            _logger.debug("pool '{}' CLEARED.".format(self.name), __name__)

    def cleanup(self):
        """Cleanup outdated items from the cache.
        """
        deleted_n = self._collection.delete_many({'expires': {'$lt': _datetime.now()}}).deleted_count

        if _reg.get('cache.debug'):
            _logger.debug("Pool '{}' CLEANED UP. Deleted {} items.".format(self.name, deleted_n), __name__)
