"""PytSite JS API.
"""
from pytsite import assetman as _assetman, lang as _lang, router as _router

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def include(lib: str, forever=False):
    if lib == 'jquery-ui':
        _assetman.add(__name__ + '@jquery-ui/jquery-ui.min.css', forever=forever)
        _assetman.add(__name__ + '@jquery-ui/jquery-ui.min.js', forever=forever)
        _assetman.add(__name__ + '@jquery-ui/i18n/datepicker-{}.js'.format(_lang.get_current_lang()), forever=forever)
    elif lib == 'bootstrap':
        include('font-awesome', forever=forever)
        _assetman.add(__name__ + '@bootstrap/css/bootstrap.min.css', forever=forever)
        _assetman.add(__name__ + '@bootstrap/css/add-columns.css', forever=forever)
        _assetman.add(__name__ + '@bootstrap/css/add-texts.css', forever=forever)
        _assetman.add(__name__ + '@bootstrap/js/bootstrap.min.js', forever=forever)
    elif lib == 'bootstrap-table':
        _assetman.add(__name__ + '@bootstrap-table/bootstrap-table.min.css', forever=forever)
        _assetman.add(__name__ + '@bootstrap-table/bootstrap-table.min.js', forever=forever)
        current_lang = _lang.get_current_lang()
        locale = current_lang + '-' + current_lang.upper()
        if current_lang == 'uk':
            locale = 'uk-UA'
        _assetman.add(__name__ + '@bootstrap-table/locale/bootstrap-table-{}.min.js'. format(locale), forever=forever)
    elif lib == 'font-awesome':
        _assetman.add(__name__ + '@font-awesome/css/font-awesome.min.css', forever=forever)
    elif lib == 'imagesloaded':
        _assetman.add(__name__ + '@js/imagesloaded.pkgd.min.js', forever=forever)
    elif lib == 'inputmask':
        _assetman.add(__name__ + '@js/jquery.inputmask.bundle.min.js', forever=forever)
    elif lib == 'typeahead':
        include('jquery-ui', forever=forever)
        _assetman.add(__name__ + '@js/typeahead.bundle.min.js', forever=forever)
    elif lib == 'tokenfield':
        include('typeahead', forever=forever)
        _assetman.add(__name__ + '@tokenfield/css/tokenfield-typeahead.min.css', forever=forever)
        _assetman.add(__name__ + '@tokenfield/bootstrap-tokenfield.min.js', forever=forever)
        _assetman.add(__name__ + '@tokenfield/css/bootstrap-tokenfield.min.css', forever=forever)
    elif lib == 'datetimepicker':
        _assetman.add(__name__ + '@datetimepicker/jquery.datetimepicker.js', forever=forever)
        _assetman.add(__name__ + '@datetimepicker/jquery.datetimepicker.css', forever=forever)
    elif lib == 'responsive':
        _assetman.add(__name__ + '@js/responsive.js', forever=forever)
    else:
        raise Exception("Unknown library: '{}'.".format(lib))

_router.add_rule('/pytsite/browser/<string:ep>', 'pytsite.browser.ep.request', methods=('GET', 'POST'))

_assetman.register_package(__name__)

_assetman.add(__name__ + '@js/jquery-2.1.4.min.js', forever=True)
_assetman.add(__name__ + '@js/common.js', forever=True)
_assetman.add(__name__ + '@js/lang.js', forever=True)
_assetman.add('app@js/translations.js', forever=True)
