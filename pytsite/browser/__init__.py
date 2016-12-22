"""PytSite JS API.
"""
# Public API
from ._api import register, include, get_assets

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    """Init wrapper.
    """
    from pytsite import assetman
    from . import _libs

    # Assets
    assetman.register_package(__name__)
    assetman.add(__name__ + '@pytsite/js/common.js', permanent=True, weight=-999)
    assetman.add(__name__ + '@pytsite/js/lang.js', permanent=True, weight=-998)

    # Libraries available out of the box
    register('jquery', _libs.jquery)
    register('jquery-ui', _libs.jquery_ui)
    register('font-awesome', _libs.font_awesome)
    register('bootstrap', _libs.bootstrap)
    register('imagesloaded', _libs.imagesloaded)
    register('inputmask', _libs.inputmask)
    register('typeahead', _libs.typeahead)
    register('tokenfield', _libs.tokenfield)
    register('datetimepicker', _libs.datetimepicker)
    register('throttle', _libs.throttle)
    register('responsive', _libs.responsive)
    register('animate', _libs.animate)
    register('wow', _libs.wow)
    register('mousewheel', _libs.mousewheel)
    register('scrollto', _libs.scrollto)
    register('waypoints', _libs.waypoints)
    register('slippry', _libs.slippry)
    register('slick', _libs.slick)
    register('select2', _libs.select2)
    register('gotop', _libs.gotop)
    register('highlight', _libs.highlight)
    register('magnific-popup', _libs.magnific_popup)
    register('js-cookie', _libs.js_cookie)

    # jQuery is ultimately required
    include('jquery', permanent=True)


_init()
