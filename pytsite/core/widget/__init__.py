"""Pytsite Widgets Package Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite.core import assetman
    assetman.register_package(__name__)

__init()


# Public API
from . import _button as button, _input as input, _select as select, _static as static
from ._base import Base
