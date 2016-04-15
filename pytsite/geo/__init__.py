"""PytSite Geo Package
"""
# Public API
from . import _widget as widget, _field as field, _validation_rule as validation_rule, _interface as interface

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import assetman, lang

    lang.register_package(__name__)
    assetman.register_package(__name__)


__init()
