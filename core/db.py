"""Database Connection.
"""

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pytsite.core import util, reg

__client = None
__database = None


def get_client() -> MongoClient:
    """Get client.
    """

    global __client
    if __client:
        return __client

    default = {
        'host': 'localhost',
        'port': 27017,
    }

    config = util.dict_merge(default, reg.get('db', {}))

    __client = MongoClient(config['host'], config['port'])

    return __client


def get_database() -> Database:
    """Get database.
    """

    global __database
    if __database:
        return __database

    __database = get_client().get_database(reg.get('db.database', 'test'))

    return __database


def get_collection(name: str) -> Collection:
    """Get collection.
    """
    return get_database().get_collection(name)
