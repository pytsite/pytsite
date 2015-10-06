"""PytSite MetaTag Module.
"""
from ._functions import dump, dump_all, get, reset, t_set
from pytsite import lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


_lang.register_package(__name__)
