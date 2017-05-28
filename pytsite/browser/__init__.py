"""PytSite JS API.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    """Init wrapper.
    """
    from pytsite import assetman, reg

    debug = reg.get('debug', False)

    # Assets
    assetman.register_package(__name__)
    assetman.t_css(__name__ + '@**')
    assetman.t_js(__name__ + '@**')
    assetman.t_copy_static(__name__ + '@**')

    # PytSite Responsive
    assetman.js_module('pytsite-responsive', __name__ + '@pytsite-responsive/pytsite-responsive')

    # jQuery
    assetman.js_module('jquery', __name__ + '@jquery/jquery')

    # jQuery UI
    assetman.js_module('jquery-ui-main', __name__ + '@jquery-ui/jquery-ui')
    assetman.js_module('jquery-ui', __name__ + '@jquery-ui/index')

    # jQuery Mousewheel
    assetman.js_module('jquery-mousewheel', __name__ + '@jquery-mousewheel/jquery.mousewheel')

    # jQuery ScrollTo
    assetman.js_module('jquery-scroll-to', __name__ + '@jquery-scroll-to/jquery.scrollTo')

    # jQuery Inputmask
    assetman.js_module('jquery-inputmask', __name__ + '@jquery-inputmask/jquery.inputmask.bundle')

    # jQuery Date Time Picker
    assetman.js_module('jquery-date-time-picker', __name__ + '@jquery-date-time-picker/jquery.datetimepicker')

    # jQuery Color Picker
    assetman.js_module('jquery-color-picker', __name__ + '@jquery-color-picker/jquery.colorpicker')

    # jQuery GoTop
    assetman.js_module('jquery-gotop', __name__ + '@jquery-gotop/jquery-gotop')

    # JS Cookie
    assetman.js_module('cookie', __name__ + '@cookie/js.cookie')

    # Font Awesome
    assetman.js_module('font-awesome', __name__ + '@font-awesome/font-awesome')
    assetman.library('font-awesome', [
        'pytsite.browser@font-awesome/css/font-awesome.css'
    ])

    # Twitter Bootstrap
    assetman.js_module('twitter-bootstrap', __name__ + '@twitter-bootstrap/twitter-bootstrap')
    assetman.library('twitter-bootstrap', [
        'pytsite.browser@twitter-bootstrap/css/bootstrap.css',
        'pytsite.browser@twitter-bootstrap/css/add-columns.css',
        'pytsite.browser@twitter-bootstrap/css/add-ons.css',
    ])

    # Twitter Bootstrap Table plugin
    assetman.js_module('twitter-bootstrap-table', __name__ + '@twitter-bootstrap-table/module')

    # Twitter Bootstrap Tokenfield plugin
    assetman.js_module('twitter-bootstrap-tokenfield-main',
                       __name__ + '@twitter-bootstrap-tokenfield/bootstrap-tokenfield')
    assetman.js_module('twitter-bootstrap-tokenfield', __name__ + '@twitter-bootstrap-tokenfield/index')

    # Twitter Typeahead
    assetman.js_module('bloodhound', __name__ + '@typeahead/bloodhound')
    assetman.js_module('typeahead-main', __name__ + '@typeahead/typeahead.jquery')
    assetman.js_module('typeahead', __name__ + '@typeahead/typeahead')

    # Select2
    assetman.js_module('select2-main', __name__ + '@select2/select2.full')
    assetman.js_module('select2', __name__ + '@select2/index')

    # Canvas to Blob
    assetman.js_module('canvas-to-blob', __name__ + '@canvas-to-blob/canvas-to-blob')

    # Load Image
    assetman.js_module('load-image', __name__ + '@load-image/load-image')
    assetman.js_module('load-image-exif', __name__ + '@load-image/load-image-exif')
    assetman.js_module('load-image-exif-map', __name__ + '@load-image/load-image-exif-map')
    assetman.js_module('load-image-fetch', __name__ + '@load-image/load-image-fetch')
    assetman.js_module('load-image-meta', __name__ + '@load-image/load-image-meta')
    assetman.js_module('load-image-orientation', __name__ + '@load-image/load-image-orientation')
    assetman.js_module('load-image-scale', __name__ + '@load-image/load-image-scale')

    # Vue
    assetman.js_module('vue', __name__ + ('@vue/vue' if debug else '@vue/vue.min'))


_init()
