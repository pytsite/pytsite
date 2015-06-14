"""JS API Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import router, assetman, lang

def include(lib: str, route_path: str=None):
    if lib == 'jquery_ui':
        assetman.add(__name__ + '@jquery-ui/jquery-ui.min.css', route_path)
        assetman.add(__name__ + '@jquery-ui/jquery-ui.min.js', route_path)
        assetman.add(__name__ + '@jquery-ui/i18n/datepicker-{}.js'.format(lang.get_current_lang()), route_path)
    elif lib == 'bootstrap':
        assetman.add(__name__ + '@bootstrap/css/bootstrap.min.css', route_path)
        assetman.add(__name__ + '@bootstrap/css/add-columns.css', route_path)
        assetman.add(__name__ + '@bootstrap/js/bootstrap.min.js', route_path)
    elif lib == 'bootstrap-table':
        assetman.add(__name__ + '@bootstrap-table/bootstrap-table.min.css', route_path)
        assetman.add(__name__ + '@bootstrap-table/bootstrap-table.min.js', route_path)
        current_lang = lang.get_current_lang()
        locale = current_lang + '-' + current_lang.upper()
        if current_lang == 'uk':
            locale = 'uk-UA'
        assetman.add(__name__ + '@bootstrap-table/locale/bootstrap-table-{}.min.js'. format(locale), route_path)
    elif lib == 'font-awesome':
        assetman.add(__name__ + '@font-awesome/css/font-awesome.min.css', route_path)
    elif lib == 'imagesloaded':
        assetman.add(__name__ + '@js/imagesloaded.pkgd.min.js', route_path)
    elif lib == 'inputmask':
        assetman.add(__name__ + '@js/jquery.inputmask.bundle.min.js', route_path)
    elif lib == 'typeahead':
        assetman.add(__name__ + '@js/typeahead.bundle.min.js', route_path)
    elif lib == 'tokenfield':
        assetman.add(__name__ + '@js/typeahead.bundle.min.js', route_path)
        assetman.add(__name__ + '@tokenfield/css/tokenfield-typeahead.min.css', route_path)
        assetman.add(__name__ + '@tokenfield/bootstrap-tokenfield.min.js', route_path)
        assetman.add(__name__ + '@tokenfield/css/bootstrap-tokenfield.min.css', route_path)
    elif lib == 'datetimepicker':
        assetman.add(__name__ + '@datetimepicker/jquery.datetimepicker.js', route_path)
        assetman.add(__name__ + '@datetimepicker/jquery.datetimepicker.css', route_path)
    else:
        raise Exception("Unknown library: '{}'.".format(lib))

router.add_rule('/core/js/<string:ep>', 'pytsite.core.client.eps.request', methods=('GET', 'POST'))

assetman.register_package(__name__)
assetman.add(__name__ + '@js/jquery-2.1.4.min.js', '*')
assetman.add(__name__ + '@js/common.js', '*')
assetman.add(__name__ + '@js/lang.js', '*')
assetman.add('app@js/translations.js', '*')