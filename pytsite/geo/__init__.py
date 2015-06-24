"""Geo Package Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

def __init():
    from pytsite.core import assetman, lang, tpl
    lang.register_package(__name__)
    assetman.register_package(__name__)

__init()

# Public API
from . import _widget, _field, _rule
widget = _widget
field = _field
rule = _rule
