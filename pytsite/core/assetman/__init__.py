"""Assetman Plugin Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import console as _console
from . import _commands
from ._functions import register_package, add, add_js, add_css, dump_js, dump_css

# Console commands
_console.register_command(_commands.BuildAssets())