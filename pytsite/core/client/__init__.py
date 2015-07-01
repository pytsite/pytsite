"""JS API Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router as _router, assetman as _assetman, lang as _lang


def include(lib: str, route_path: str=None):
    if lib == 'jquery_ui':
        _assetman.add(__name__ + '@jquery-ui/jquery-ui.min.css', route_path)
        _assetman.add(__name__ + '@jquery-ui/jquery-ui.min.js', route_path)
        _assetman.add(__name__ + '@jquery-ui/i18n/datepicker-{}.js'.format(_lang.get_current_lang()), route_path)
    elif lib == 'bootstrap':
        _assetman.add(__name__ + '@bootstrap/css/bootstrap.min.css', route_path)
        _assetman.add(__name__ + '@bootstrap/css/add-columns.css', route_path)
        _assetman.add(__name__ + '@bootstrap/css/add-texts.css', route_path)
        _assetman.add(__name__ + '@bootstrap/js/bootstrap.min.js', route_path)
    elif lib == 'bootstrap-table':
        _assetman.add(__name__ + '@bootstrap-table/bootstrap-table.min.css', route_path)
        _assetman.add(__name__ + '@bootstrap-table/bootstrap-table.min.js', route_path)
        current_lang = _lang.get_current_lang()
        locale = current_lang + '-' + current_lang.upper()
        if current_lang == 'uk':
            locale = 'uk-UA'
        _assetman.add(__name__ + '@bootstrap-table/locale/bootstrap-table-{}.min.js'. format(locale), route_path)
    elif lib == 'font-awesome':
        _assetman.add(__name__ + '@font-awesome/css/font-awesome.min.css', route_path)
    elif lib == 'imagesloaded':
        _assetman.add(__name__ + '@js/imagesloaded.pkgd.min.js', route_path)
    elif lib == 'inputmask':
        _assetman.add(__name__ + '@js/jquery.inputmask.bundle.min.js', route_path)
    elif lib == 'typeahead':
        _assetman.add(__name__ + '@js/typeahead.bundle.min.js', route_path)
    elif lib == 'tokenfield':
        _assetman.add(__name__ + '@js/typeahead.bundle.min.js', route_path)
        _assetman.add(__name__ + '@tokenfield/css/tokenfield-typeahead.min.css', route_path)
        _assetman.add(__name__ + '@tokenfield/bootstrap-tokenfield.min.js', route_path)
        _assetman.add(__name__ + '@tokenfield/css/bootstrap-tokenfield.min.css', route_path)
    elif lib == 'datetimepicker':
        _assetman.add(__name__ + '@datetimepicker/jquery.datetimepicker.js', route_path)
        _assetman.add(__name__ + '@datetimepicker/jquery.datetimepicker.css', route_path)
    else:
        raise Exception("Unknown library: '{}'.".format(lib))

_router.add_rule('/core/js/<string:ep>', 'pytsite.core.client.eps.request', methods=('GET', 'POST'))

_assetman.register_package(__name__)
_assetman.add(__name__ + '@js/jquery-2.1.4.min.js', '*')
_assetman.add(__name__ + '@js/common.js', '*')
_assetman.add(__name__ + '@js/lang.js', '*')
_assetman.add('app@js/translations.js', '*')