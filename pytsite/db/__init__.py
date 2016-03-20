"""Pytsite Database Module.
"""
# Public API
from pymongo import ASCENDING as I_ASC, DESCENDING as I_DESC, TEXT as I_TEXT, GEO2D as I_GEO2D
from ._api import get_client, get_collection, get_collection_names, get_config, get_database

from pytsite import console as _console, lang as _lang
from ._console_command import Db

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_lang.register_package(__name__)
_console.register_command(Db())
