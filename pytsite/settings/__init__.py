"""Settings Plugin Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


# Init wrapper
def __init():
    from pytsite.core import router, lang, odm, tpl
    from pytsite import admin, auth
    from ._model import Setting

    # Language package
    lang.register_package(__name__)

    # Template package
    tpl.register_package(__name__)

    # ODM model
    odm.register_model('setting', Setting)

    # Routing
    router.add_rule('/admin/settings/<string:uid>', 'pytsite.settings.eps.form')
    router.add_rule('/admin/settings/<string:uid>/submit', 'pytsite.settings.eps.form_submit', methods=('POST',))

    # Sidebar section
    admin.sidebar.add_section('settings', __name__ + '@settings', 2000, ('*',))

    # Auth permission group
    auth.define_permission_group('settings', 'pytsite.settings@settings')

# Package initialization
__init()

# Public API
from ._functions import define, get_setting
