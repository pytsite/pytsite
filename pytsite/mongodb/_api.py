"""PytSite Database Functions.
"""
import ssl as _ssl
from pymongo import MongoClient as _MongoClient
from pymongo.database import Database as _Database
from pymongo.collection import Collection as _Collection
from pytsite import reg as _reg, console as _console

__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_client = None
_database = None


def get_config() -> dict:
    """
    :return:
    """
    return {
        'host': _reg.get('db.host', 'localhost'),
        'port': _reg.get('db.port', 27017),
        'ssl': _reg.get('db.ssl', False),
        'database': _reg.get('db.database', 'test'),
        'user': _reg.get('db.user'),
        'password': _reg.get('db.password'),
        'connect_timeout': 5000,
        'socket_timeout': 5000,
        'server_selection_timeout': 5000,
    }


def get_client() -> _MongoClient:
    """Get client
    """
    global _client
    if _client:
        return _client

    config = get_config()

    if config['database'] == 'test':
        _console.print_warning("It seems you use default database configuration. "
                               "Consider to change value of the 'db.database' configuration parameter.")

    _client = _MongoClient(config['host'], config['port'], ssl=config['ssl'], ssl_cert_reqs=_ssl.CERT_NONE,
                           connect=False, connectTimeoutMS=config['connect_timeout'],
                           socketTimeoutMS=config['socket_timeout'],
                           serverSelectionTimeoutMS=config['server_selection_timeout'])

    return _client


def get_database() -> _Database:
    """Get database
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
    return get_database().get_collection(name)


def get_collection_names(include_system: bool = False) -> list:
    """Get existing collection names
    """
    return get_database().collection_names(include_system)
