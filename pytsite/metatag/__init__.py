"""PytSite MetaTag Module.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import lang as _lang

_lang.register_package(__name__)

# Public API
from ._functions import *
