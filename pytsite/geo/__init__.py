"""PytSite Geo Package
"""
# Public API
from . import _widget as widget, _field as field, _validation_rule as validation_rule

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite import assetman, lang

    lang.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_js(__name__ + '@**/*.js')
    assetman.js_module('pytsite-geo-widget-location', __name__ + '@js/pytsite-geo-widget-location')


__init()
