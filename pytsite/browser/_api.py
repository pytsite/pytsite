"""pytsite.browser API Functions.
"""
from pytsite import assetman as _assetman, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


__eps = {}


def include(lib: str, forever=False):
    """Add a browser library to the assetman.
    """
    if lib == 'jquery-ui':
        _assetman.add('pytsite.browser@jquery-ui/jquery-ui.min.css', forever=forever)
        _assetman.add('pytsite.browser@jquery-ui/jquery-ui.min.js', forever=forever)
        if _lang.get_current() != 'en':
            _assetman.add('pytsite.browser@jquery-ui/i18n/datepicker-{}.js'.format(_lang.get_current()), forever=forever)
    elif lib == 'bootstrap':
        include('font-awesome', forever=forever)
        _assetman.add('pytsite.browser@bootstrap/css/bootstrap.min.css', forever=forever)
        _assetman.add('pytsite.browser@bootstrap/css/add-columns.css', forever=forever)
        _assetman.add('pytsite.browser@bootstrap/css/add-texts.css', forever=forever)
        _assetman.add('pytsite.browser@bootstrap/js/bootstrap.min.js', forever=forever)
    elif lib == 'bootstrap-table':
        _assetman.add('pytsite.browser@bootstrap-table/bootstrap-table.min.css', forever=forever)
        _assetman.add('pytsite.browser@bootstrap-table/bootstrap-table.min.js', forever=forever)
        _assetman.add('pytsite.browser@bootstrap-table/extensions/cookie/bootstrap-table-cookie.min.js',
                      forever=forever)
        current_lang = _lang.get_current()
        if current_lang != 'en':
            locale = current_lang + '-' + current_lang.upper()
            if current_lang == 'uk':
                locale = 'uk-UA'
            _assetman.add('pytsite.browser@bootstrap-table/locale/bootstrap-table-{}.min.js'. format(locale),
                          forever=forever)
    elif lib == 'font-awesome':
        _assetman.add('pytsite.browser@font-awesome/css/font-awesome.min.css', forever=forever)
    elif lib == 'imagesloaded':
        _assetman.add('pytsite.browser@js/imagesloaded.pkgd.min.js', forever=forever)
    elif lib == 'inputmask':
        _assetman.add('pytsite.browser@js/jquery.inputmask.bundle.min.js', forever=forever)
    elif lib == 'typeahead':
        include('jquery-ui', forever=forever)
        _assetman.add('pytsite.browser@js/typeahead.bundle.min.js', forever=forever)
    elif lib == 'tokenfield':
        include('typeahead', forever=forever)
        _assetman.add('pytsite.browser@tokenfield/css/tokenfield-typeahead.min.css', forever=forever)
        _assetman.add('pytsite.browser@tokenfield/bootstrap-tokenfield.min.js', forever=forever)
        _assetman.add('pytsite.browser@tokenfield/css/bootstrap-tokenfield.min.css', forever=forever)
    elif lib == 'datetimepicker':
        _assetman.add('pytsite.browser@datetimepicker/jquery.datetimepicker.js', forever=forever)
        _assetman.add('pytsite.browser@datetimepicker/jquery.datetimepicker.css', forever=forever)
    elif lib == 'responsive':
        _assetman.add('pytsite.browser@js/responsive.js', forever=forever)
    elif lib == 'animate':
        _assetman.add('pytsite.browser@css/animate.css', forever=forever)
    elif lib == 'wow':
        include('animate', forever=forever)
        _assetman.add('pytsite.browser@js/wow.min.js', forever=forever)
    elif lib == 'mousewheel':
        _assetman.add('pytsite.browser@js/jquery.mousewheel.min.js', forever=forever)
    elif lib == 'smoothscroll':
        include('mousewheel', forever=forever)
        _assetman.add('pytsite.browser@js/jquery.simplr.smoothscroll.min.js', forever=forever)
        _assetman.add('pytsite.browser@js/smoothscroll-init.js', forever=forever)
    elif lib == 'enllax':
        _assetman.add('pytsite.browser@js/jquery.enllax.min.js', forever=forever)
    elif lib == 'scrollto':
        _assetman.add('pytsite.browser@js/jquery.scrollTo.min.js', forever=forever)
    elif lib == 'waypoints':
        _assetman.add('pytsite.browser@js/jquery.waypoints.min.js', forever=forever)
    elif lib == 'slippry':
        _assetman.add('pytsite.browser@js/slippry.min.js', forever=forever)
        _assetman.add('pytsite.browser@css/slippry.css', forever=forever)
    elif lib == 'select2':
        include('mousewheel', forever=forever)
        _assetman.add('pytsite.browser@select2/js/select2.full.min.js', forever=forever)
        _assetman.add('pytsite.browser@select2/js/i18n/{}.js'.format(_lang.get_current()), forever=forever)
        _assetman.add('pytsite.browser@select2/css/select2.min.css', forever=forever)
        _assetman.add('pytsite.browser@select2/css/select2-bootstrap.min.css', forever=forever)
    else:
        raise Exception("Unknown library: '{}'.".format(lib))


def is_ep_registered(ep_name: str) -> bool:
    """Check if the endpoint is registered.
    """
    return ep_name in __eps


def register_ep(ep_name: str):
    """Register an endpoint.
    """
    if is_ep_registered(ep_name):
        raise Exception("Endpoint '{}' is already registered.".format(ep_name))

    __eps[ep_name] = ep_name
