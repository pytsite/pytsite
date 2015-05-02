from . import registry, helpers
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

__client = None
__database = None


def get_client()->MongoClient:
    global __client

    if __client is not None:
        return __client

    default = {
        'host': 'localhost',
        'port': 27017,
    }
    config = helpers.dict_merge(default, registry.get_val('db', {}))

    __client = MongoClient(config['host'], config['port'])

    return __client


def get_database()->Database:
    global __database

    if __database is not None:
        return __database

    __database = get_client().get_database(registry.get_val('db.database', 'test'))

    return __database


def get_collection(name: str)->Collection:
    return get_database().get_collection(name)