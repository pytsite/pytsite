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
from . import _base, _button, _input, _select, _static, _wysiwyg
base = _base
button = _button
input = _input
select = _select
static = _static
wysiwyg = _wysiwyg
