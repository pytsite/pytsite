"""JS API Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router as _router, assetman as _assetman, lang as _lang


def include(lib: str):
    _assetman.add(__name__ + '@js/common.js')
    _assetman.add(__name__ + '@js/lang.js')
    _assetman.add('app@js/translations.js')

    if lib == 'jquery':
        _assetman.add(__name__ + '@js/jquery-2.1.4.min.js')
    elif lib == 'jquery-ui':
        include('jquery')
        _assetman.add(__name__ + '@jquery-ui/jquery-ui.min.css')
        _assetman.add(__name__ + '@jquery-ui/jquery-ui.min.js')
        _assetman.add(__name__ + '@jquery-ui/i18n/datepicker-{}.js'.format(_lang.get_current_lang()))
    elif lib == 'bootstrap':
        include('jquery')
        _assetman.add(__name__ + '@bootstrap/css/bootstrap.min.css')
        _assetman.add(__name__ + '@bootstrap/css/add-columns.css')
        _assetman.add(__name__ + '@bootstrap/css/add-texts.css')
        _assetman.add(__name__ + '@bootstrap/js/bootstrap.min.js')
    elif lib == 'bootstrap-table':
        include('jquery')
        _assetman.add(__name__ + '@bootstrap-table/bootstrap-table.min.css')
        _assetman.add(__name__ + '@bootstrap-table/bootstrap-table.min.js')
        current_lang = _lang.get_current_lang()
        locale = current_lang + '-' + current_lang.upper()
        if current_lang == 'uk':
            locale = 'uk-UA'
        _assetman.add(__name__ + '@bootstrap-table/locale/bootstrap-table-{}.min.js'. format(locale))
    elif lib == 'font-awesome':
        _assetman.add(__name__ + '@font-awesome/css/font-awesome.min.css')
    elif lib == 'imagesloaded':
        _assetman.add(__name__ + '@js/imagesloaded.pkgd.min.js')
    elif lib == 'inputmask':
        include('jquery')
        _assetman.add(__name__ + '@js/jquery.inputmask.bundle.min.js')
    elif lib == 'typeahead':
        include('jquery-ui')
        _assetman.add(__name__ + '@js/typeahead.bundle.min.js')
    elif lib == 'tokenfield':
        include('typeahead')
        _assetman.add(__name__ + '@tokenfield/css/tokenfield-typeahead.min.css')
        _assetman.add(__name__ + '@tokenfield/bootstrap-tokenfield.min.js')
        _assetman.add(__name__ + '@tokenfield/css/bootstrap-tokenfield.min.css')
    elif lib == 'datetimepicker':
        include('jquery')
        _assetman.add(__name__ + '@datetimepicker/jquery.datetimepicker.js')
        _assetman.add(__name__ + '@datetimepicker/jquery.datetimepicker.css')
    else:
        raise Exception("Unknown library: '{}'.".format(lib))

_router.add_rule('/core/js/<string:ep>', 'pytsite.core.browser.eps.request', methods=('GET', 'POST'))

_assetman.register_package(__name__)