"""Pytsite Widgets Package Init.
"""
# Public API
from . import _button as button, _input as input, _select as select, _static as static, _misc as misc
from ._base import Abstract, Container, MultiRow

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import assetman, tpl, lang
    lang.register_package(__name__)
    tpl.register_package(__name__)

    assetman.register_package(__name__)
    assetman.t_copy(__name__ + '@bootstrap-table/**/*', 'bootstrap-table')
    assetman.t_copy(__name__ + '@jquery-color-picker/**/*', 'jquery-color-picker')
    assetman.t_less(__name__ + '@css/*', 'css')
    assetman.t_js(__name__ + '@js/*', 'js')

    assetman.js_module('pytsite-widget', __name__ + '@js/widget')
    assetman.js_module('pytsite-widget-input-text', __name__ + '@js/text')
    assetman.js_module('pytsite-widget-input-typeahead-text', __name__ + '@js/typeahead-text')
    assetman.js_module('pytsite-widget-input-integer', __name__ + '@js/integer')
    assetman.js_module('pytsite-widget-input-string-list', __name__ + '@js/string-list')
    assetman.js_module('pytsite-widget-input-tokens', __name__ + '@js/tokens')
    assetman.js_module('pytsite-widget-select-select2', __name__ + '@js/select2')
    assetman.js_module('pytsite-widget-select-date-time', __name__ + '@js/date-time')
    assetman.js_module('pytsite-widget-misc-bootstrap-table', __name__ + '@js/bootstrap-table')


_init()
