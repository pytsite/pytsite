"""PytSite Database Functions.
"""
import ssl as _ssl
from pymongo import MongoClient as _MongoClient
from pymongo.database import Database as _Database
from pymongo.collection import Collection as _Collection
from pymongo.errors import ServerSelectionTimeoutError
from pytsite import util as _util, reg as _reg, logger as _logger

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_client = None
_database = None


def get_config() -> dict:
    return {
        'host': _reg.get('db.host', 'localhost'),
        'port': _reg.get('db.port', 27017),
        'ssl': _reg.get('db.ssl', False),
        'database': _reg.get('db.database', 'test'),
        'user': _reg.get('db.user'),
        'password': _reg.get('db.password'),
    }


def get_client() -> _MongoClient:
    """Get client.
    """
    global _client
    if _client:
        return _client

    config = get_config()
    _client = _MongoClient(config['host'], config['port'], ssl=config['ssl'], ssl_cert_reqs=_ssl.CERT_NONE,
                           connect=False)

    return _client


def get_database() -> _Database:
    """Get database.
    """
    global _database
    if _database:
        return _database

    config = get_config()
    _database = get_client().get_database(config['database'])

    if config['user']:
        _database.authenticate(config['user'], config['password'])

    return _database


def get_collection(name: str) -> _Collection:
    """Get collection.
    """
    try:
        return get_database().get_collection(name)
    except ServerSelectionTimeoutError as e:
        global _client, _database
        _client = None
        _database = None
        _logger.error("Error while getting collection '{}': {}.".format(name, e), exc_info=e)

        return get_collection(name)


def get_collection_names(include_system: bool=False) -> list:
    """Get existing collection names.
    """
    try:
        return get_database().collection_names(include_system)
    except ServerSelectionTimeoutError as e:
        global _client, _database
        _client = None
        _database = None
        _logger.error("Error while getting collection names: {}.".format(e), exc_info=e)

        return get_collection_names(include_system)
