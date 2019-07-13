"""PytSite MongoDB SUpport API Functions
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import ssl
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pytsite import reg, console

_client = None
_database = None


def get_config() -> dict:
    """
    :return:
    """
    return {
        'host': reg.get('db.host', 'localhost'),
        'port': reg.get('db.port', 27017),
        'ssl': reg.get('db.ssl', False),
        'database': reg.get('db.database', 'test'),
        'user': reg.get('db.user'),
        'password': reg.get('db.password'),
        'connect_timeout': 5000,
        'socket_timeout': 5000,
        'server_selection_timeout': 5000,
    }


def get_client() -> MongoClient:
    """Get client
    """
    global _client
    if _client:
        return _client

    config = get_config()

    if config['database'] == 'test':
        console.print_warning("It seems you use default database configuration. "
                              "Consider to change value of the 'db.database' configuration parameter.")

    _client = MongoClient(config['host'], config['port'], ssl=config['ssl'], ssl_cert_reqs=ssl.CERT_NONE,
                          connect=False, connectTimeoutMS=config['connect_timeout'],
                          socketTimeoutMS=config['socket_timeout'],
                          serverSelectionTimeoutMS=config['server_selection_timeout'])

    return _client


def get_database() -> Database:
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


def get_collection(name: str) -> Collection:
    """Get collection.
    """
    return get_database().get_collection(name)


def get_collection_names(include_system: bool = False) -> list:
    """Get existing collection names
    """
    return get_database().collection_names(include_system)
