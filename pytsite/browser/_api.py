"""pytsite.browser API Functions.
"""
from typing import Callable as _Callable
from pytsite import assetman as _assetman, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__libraries = {}


def register(lib: str, callback: _Callable):
    """Register a library.
    """
    if lib in __libraries:
        raise KeyError("Browser library '{}' is already registered.".format(lib))

    __libraries[lib] = callback


def include(lib: str, permanent=False, **kwargs):
    """Include a library.
    """
    if lib == 'jquery':
        _assetman.add('pytsite.browser@js/jquery-2.1.4.min.js', permanent=permanent)
    elif lib == 'jquery-ui':
        include('jquery')
        _assetman.add('pytsite.browser@jquery-ui/jquery-ui.min.css', permanent=permanent)
        _assetman.add('pytsite.browser@jquery-ui/jquery-ui.min.js', permanent=permanent)
        if _lang.get_current() != 'en':
            _assetman.add('pytsite.browser@jquery-ui/i18n/datepicker-{}.js'.format(_lang.get_current()),
                          permanent=permanent)
    elif lib == 'jquery-mobile':
        include('jquery')
        _assetman.add('pytsite.browser@jquery-mobile/jquery.mobile-1.4.5.min.css')
        _assetman.add('pytsite.browser@jquery-mobile/jquery.mobile-1.4.5.min.js')
    elif lib == 'font-awesome':
        _assetman.add('pytsite.browser@font-awesome/css/font-awesome.min.css', permanent=permanent)
    elif lib == 'bootstrap':
        include('font-awesome', permanent=permanent)
        _assetman.add('pytsite.browser@bootstrap/css/bootstrap.min.css', permanent=permanent)
        _assetman.add('pytsite.browser@bootstrap/css/add-columns.css', permanent=permanent)
        _assetman.add('pytsite.browser@bootstrap/css/add-ons.css', permanent=permanent)
        _assetman.add('pytsite.browser@bootstrap/js/bootstrap.min.js', permanent=permanent)
    elif lib == 'bootstrap-table':
        _assetman.add('pytsite.browser@bootstrap-table/bootstrap-table.min.css', permanent=permanent)
        _assetman.add('pytsite.browser@bootstrap-table/bootstrap-table.min.js', permanent=permanent)
        _assetman.add('pytsite.browser@bootstrap-table/extensions/cookie/bootstrap-table-cookie.min.js',
                      permanent=permanent)
        current_lang = _lang.get_current()
        if current_lang != 'en':
            locale = current_lang + '-' + current_lang.upper()
            if current_lang == 'uk':
                locale = 'uk-UA'
            _assetman.add('pytsite.browser@bootstrap-table/locale/bootstrap-table-{}.min.js'. format(locale),
                          permanent=permanent)
    elif lib == 'imagesloaded':
        _assetman.add('pytsite.browser@js/imagesloaded.pkgd.min.js', permanent=permanent)
    elif lib == 'inputmask':
        _assetman.add('pytsite.browser@js/jquery.inputmask.bundle.min.js', permanent=permanent)
    elif lib == 'typeahead':
        include('jquery-ui', permanent=permanent)
        _assetman.add('pytsite.browser@typeahead/typeahead.css', permanent=permanent)
        _assetman.add('pytsite.browser@typeahead/typeahead.bundle.min.js', permanent=permanent)
    elif lib == 'tokenfield':
        include('typeahead', permanent=permanent)
        _assetman.add('pytsite.browser@tokenfield/css/tokenfield-typeahead.css', permanent=permanent)
        _assetman.add('pytsite.browser@tokenfield/bootstrap-tokenfield.min.js', permanent=permanent)
        _assetman.add('pytsite.browser@tokenfield/css/bootstrap-tokenfield.css', permanent=permanent)
    elif lib == 'datetimepicker':
        _assetman.add('pytsite.browser@datetimepicker/jquery.datetimepicker.js', permanent=permanent)
        _assetman.add('pytsite.browser@datetimepicker/jquery.datetimepicker.css', permanent=permanent)
    elif lib == 'throttle':
        _assetman.add('pytsite.browser@js/jquery.ba-throttle-debounce.min.js', permanent=permanent)
    elif lib == 'responsive':
        include('throttle', permanent=permanent)
        _assetman.add('pytsite.browser@pytsite/js/responsive.js', permanent=permanent)
    elif lib == 'animate':
        _assetman.add('pytsite.browser@css/animate.css', permanent=permanent)
    elif lib == 'wow':
        include('animate', permanent=permanent)
        _assetman.add('pytsite.browser@js/wow.min.js', permanent=permanent)
    elif lib == 'mousewheel':
        _assetman.add('pytsite.browser@js/jquery.mousewheel.min.js', permanent=permanent)
    elif lib == 'smoothscroll':
        include('mousewheel', permanent=permanent)
        _assetman.add('pytsite.browser@js/jquery.simplr.smoothscroll.min.js', permanent=permanent)
        _assetman.add('pytsite.browser@js/smoothscroll-init.js', permanent=permanent)
    elif lib == 'enllax':
        _assetman.add('pytsite.browser@js/jquery.enllax.min.js', permanent=permanent)
    elif lib == 'scrollto':
        _assetman.add('pytsite.browser@js/jquery.scrollTo.min.js', permanent=permanent)
    elif lib == 'waypoints':
        _assetman.add('pytsite.browser@js/jquery.waypoints.min.js', permanent=permanent)
    elif lib == 'slippry':
        _assetman.add('pytsite.browser@slippry/slippry.min.js', permanent=permanent)
        _assetman.add('pytsite.browser@slippry/slippry.css', permanent=permanent)
    elif lib == 'slick':
        _assetman.add('pytsite.browser@slick/slick.min.js', permanent=permanent)
        _assetman.add('pytsite.browser@slick/slick.css', permanent=permanent)
        _assetman.add('pytsite.browser@slick/slick-theme.css', permanent=permanent)
    elif lib == 'select2':
        include('mousewheel', permanent=permanent)
        _assetman.add('pytsite.browser@select2/js/select2.full.min.js', permanent=permanent)
        _assetman.add('pytsite.browser@select2/js/i18n/{}.js'.format(_lang.get_current()), permanent=permanent)
        _assetman.add('pytsite.browser@select2/css/select2.min.css', permanent=permanent)
        _assetman.add('pytsite.browser@select2/css/select2-bootstrap.min.css', permanent=permanent)
    elif lib == 'gotop':
        _assetman.add('pytsite.browser@js/jquery.gotop.min.js', permanent=permanent)
    elif lib == 'highlight':
        _assetman.add('pytsite.browser@highlight/styles/' + kwargs.get('style', 'default') + '.css')
        _assetman.add('pytsite.browser@highlight/highlight.pack.js', permanent=permanent)
    elif lib in __libraries:
        # Call external callback
        __libraries[lib](permanent, **kwargs)
    else:
        raise ValueError("Unknown library: '{}'.".format(lib))
