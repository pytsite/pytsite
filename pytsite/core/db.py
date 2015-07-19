"""Database Connection.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pymongo import MongoClient as _MongoClient
from pymongo.database import Database as _Database
from pymongo.collection import Collection as _Collection
from pytsite.core import util as _util, reg as _reg


__client = None
__database = None


def _get_config() -> dict:
    default = {
        'host': 'localhost',
        'port': 27017,
        'database': 'test',
        'user': None,
        'password': None,
        'ssl': False,
    }

    return _util.dict_merge(default, _reg.get('db', {}))


def get_client() -> _MongoClient:
    """Get client.
    """
    global __client
    if __client:
        return __client

    config = _get_config()
    __client = _MongoClient(config['host'], config['port'])

    return __client


def get_database() -> _Database:
    """Get database.
    """
    global __database
    if __database:
        return __database

    config = _get_config()
    __database = get_client().get_database(config['database'])

    if config['user']:
        __database.authenticate(config['user'], config['password'])

    return __database


def get_collection(name: str) -> _Collection:
    """Get collection.
    """
    return get_database().get_collection(name)


def get_collection_names(include_system: bool=False) -> list:
    """Get existing collection names.
    """
    return get_database().collection_names(include_system)
