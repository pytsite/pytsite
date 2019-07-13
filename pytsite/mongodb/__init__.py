"""PytSite MongoDB Support
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Public API
from pymongo import ASCENDING as I_ASC, DESCENDING as I_DESC, TEXT as I_TEXT, GEO2D as I_GEO2D
from ._api import get_client, get_collection, get_collection_names, get_config, get_database


def _init():
    from pytsite import console, lang
    from . import _console_command

    lang.register_package(__name__)
    console.register_command(_console_command.Db())


_init()
