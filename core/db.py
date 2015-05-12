__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pymongo import MongoClient as __MongoClient
from pymongo.database import Database as __Database
from pymongo.collection import Collection as __Collection

__client = None
__database = None


def get_client()->__MongoClient:
    """Get client.
    """
    global __client

    if __client:
        return __client

    default = {
        'host': 'localhost',
        'port': 27017,
    }

    from pytsite.core import utils, registry
    config = utils.dict_merge(default, registry.get_val('db', {}))

    __client = __MongoClient(config['host'], config['port'])

    return __client


def get_database()->__Database:
    """Get database.
    """
    global __database

    if __database is not None:
        return __database

    from pytsite.core import registry
    __database = get_client().get_database(registry.get_val('db.database', 'test'))

    return __database


def get_collection(name: str)->__Collection:
    """Get collection.
    """
    return get_database().get_collection(name)