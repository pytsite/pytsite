"""PytSite Browser Core Libraries.
"""
from pytsite import lang as _lang
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def jquery() -> list:
    return ['pytsite.browser@js/jquery-2.1.4.min.js']


def jquery_ui() -> list:
    r = [
        'pytsite.browser@jquery-ui/jquery-ui.min.css',
        'pytsite.browser@jquery-ui/jquery-ui.min.js',
    ]

    if _lang.get_current() != 'en':
        r.append('pytsite.browser@jquery-ui/i18n/datepicker-{}.js'.format(_lang.get_current()))

    return r


def font_awesome() -> list:
    return ['pytsite.browser@font-awesome/css/font-awesome.min.css']


def bootstrap() -> list:
    r = _api.get_assets('font-awesome')
    r.extend([
        'pytsite.browser@bootstrap/css/bootstrap.min.css',
        'pytsite.browser@bootstrap/css/add-columns.css',
        'pytsite.browser@bootstrap/css/add-ons.css',
        'pytsite.browser@bootstrap/js/bootstrap.min.js',
    ])

    return r


def imagesloaded() -> list:
    return ['pytsite.browser@js/imagesloaded.pkgd.min.js']


def inputmask() -> list:
    return ['pytsite.browser@js/jquery.inputmask.bundle.min.js']


def typeahead() -> list:
    r = _api.get_assets('jquery-ui')
    r.extend([
        'pytsite.browser@typeahead/typeahead.css',
        'pytsite.browser@typeahead/typeahead.bundle.min.js'
    ])

    return r


def tokenfield() -> list:
    r = _api.get_assets('typeahead')
    r.extend([
        'pytsite.browser@tokenfield/css/tokenfield-typeahead.css',
        'pytsite.browser@tokenfield/bootstrap-tokenfield.min.js',
        'pytsite.browser@tokenfield/css/bootstrap-tokenfield.css',
    ])

    return r


def datetimepicker() -> list:
    return [
        'pytsite.browser@datetimepicker/jquery.datetimepicker.js',
        'pytsite.browser@datetimepicker/jquery.datetimepicker.css',
    ]


def throttle() -> list:
    return ['pytsite.browser@js/jquery.ba-throttle-debounce.min.js']


def responsive() -> list:
    return ['pytsite.browser@pytsite/js/responsive.js']


def animate() -> list:
    return ['pytsite.browser@css/animate.css']


def wow() -> list:
    r = _api.get_assets('animate')
    r.extend(['pytsite.browser@js/wow.min.js'])

    return r


def mousewheel() -> list:
    return ['pytsite.browser@js/jquery.mousewheel.min.js']


def scrollto() -> list:
    return ['pytsite.browser@js/jquery.scrollTo.min.js']


def waypoints() -> list:
    return ['pytsite.browser@js/jquery.waypoints.min.js']


def slippry() -> list:
    return [
        'pytsite.browser@slippry/slippry.min.js',
        'pytsite.browser@slippry/slippry.css',
    ]


def slick() -> list:
    return [
        'pytsite.browser@slick/slick.min.js',
        'pytsite.browser@slick/slick.css',
        'pytsite.browser@slick/slick-theme.css'
    ]


def select2() -> list:
    r = _api.get_assets('mousewheel')
    r.extend([
        'pytsite.browser@select2/js/select2.full.min.js',
        'pytsite.browser@select2/js/i18n/{}.js'.format(_lang.get_current()),
        'pytsite.browser@select2/css/select2.min.css',
        'pytsite.browser@select2/css/select2-bootstrap.min.css',
    ])

    return r


def gotop() -> list:
    return ['pytsite.browser@js/jquery.gotop.min.js']


def highlight(**kwargs):
    return [
        'pytsite.browser@highlight/styles/' + kwargs.get('style', 'default') + '.css',
        'pytsite.browser@highlight/highlight.pack.js',
    ]


def magnific_popup():
    return [
        'pytsite.browser@magnific-popup/magnific-popup.css',
        'pytsite.browser@magnific-popup/jquery.magnific-popup.min.js',
    ]


def js_cookie():
    return [
        'pytsite.browser@js/js.cookie.js'
    ]
