"""Widgets Package.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    from pytsite.core import assetman
    assetman.register_package(__name__)

__init()

# Public API
from . import _abstract, _button, _input, _select, _static, _wrapper, _wysiwyg
base = _abstract
button = _button
input = _input
select = _select
static = _static
wrapper = _wrapper
wysiwyg = _wysiwyg
