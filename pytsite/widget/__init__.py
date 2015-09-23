"""Pytsite Widgets Package Init.
"""
# Public API
from . import _button as button, _input as input, _select as select, _static as static
from ._base import Base

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import assetman
    from pytsite import tpl
    from pytsite import lang
    assetman.register_package(__name__)
    tpl.register_package(__name__)
    lang.register_package(__name__)

__init()
