"""Pytsite Database Module.
"""
from pytsite import console as _console, lang as _lang
from ._console_commands import DbDump, DbRestore

# Public API
from ._function import get_client, get_collection, get_collection_names, get_config, get_database

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_lang.register_package(__name__)
_console.register_command(DbDump())
_console.register_command(DbRestore())
