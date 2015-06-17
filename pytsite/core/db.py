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


def get_client() -> _MongoClient:
    """Get client.
    """

    global __client
    if __client:
        return __client

    default = {
        'host': 'localhost',
        'port': 27017,
    }

    config = _util.dict_merge(default, _reg.get('db', {}))

    __client = _MongoClient(config['host'], config['port'])

    return __client


def get_database() -> _Database:
    """Get database.
    """

    global __database
    if __database:
        return __database

    __database = get_client().get_database(_reg.get('db.database', 'test'))

    return __database


def get_collection(name: str) -> _Collection:
    """Get collection.
    """
    return get_database().get_collection(name)
