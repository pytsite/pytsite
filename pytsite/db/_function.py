"""PytSite Database Functions.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import ssl
from pymongo import MongoClient as _MongoClient
from pymongo.database import Database as _Database
from pymongo.collection import Collection as _Collection
from pymongo.errors import ServerSelectionTimeoutError
from pytsite import util as _util, reg as _reg
from pytsite import logger as _logger

__client = None
__database = None


def get_config() -> dict:
    default = {
        'host': 'localhost',
        'port': 27017,
        'ssl': True,
        'database': 'test',
        'user': None,
        'password': None,
    }

    return _util.dict_merge(default, _reg.get('db', {}))


def get_client() -> _MongoClient:
    """Get client.
    """
    global __client
    if __client:
        return __client

    config = get_config()
    __client = _MongoClient(config['host'], config['port'], ssl=config['ssl'], ssl_cert_reqs=ssl.CERT_NONE)

    return __client


def get_database() -> _Database:
    """Get database.
    """
    global __database
    if __database:
        return __database

    config = get_config()
    __database = get_client().get_database(config['database'])

    if config['user']:
        __database.authenticate(config['user'], config['password'])

    return __database


def get_collection(name: str) -> _Collection:
    """Get collection.
    """
    try:
        return get_database().get_collection(name)
    except ServerSelectionTimeoutError:
        global __client, __database
        __client = None
        __database = None
        _logger.error('Connection lost.', __name__)
        return get_collection(name)


def get_collection_names(include_system: bool=False) -> list:
    """Get existing collection names.
    """
    try:
        return get_database().collection_names(include_system)
    except ServerSelectionTimeoutError:
        global __client, __database
        __client = None
        __database = None
        _logger.error('Connection lost.', __name__)
        return get_collection_names(include_system)
