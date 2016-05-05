"""Pytsite Widgets Package Init.
"""
# Public API
from . import _button as button, _input as input, _select as select, _static as static
from ._base import Base, Container

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite import assetman, tpl, lang
    assetman.register_package(__name__)
    lang.register_package(__name__)
    tpl.register_package(__name__)

    assetman.add('pytsite.widget@js/widget.js', True)
    assetman.add('pytsite.widget@css/widget.css', True)

__init()
