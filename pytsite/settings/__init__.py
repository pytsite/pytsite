"""Settings Plugin Init.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


# Public API
from ._functions import define_setting

# Init wrapper
def __init():
    from pytsite.core import router, lang, odm
    from pytsite import admin
    from ._models import SettingModel

    # Language package
    lang.register_package(__name__)

    # ODM model
    odm.manager.register_model('setting', SettingModel)

    # Routing
    router.add_rule('/admin/settings/<string:uid>', 'pytsite.settings.eps.form')
    router.add_rule('/admin/settings/<string:uid>/submit', 'pytsite.settings.eps.form_submit')

    # Sidebar section
    admin.sidebar.add_section('settings', __name__ + '@settings', 2000, ('*',))

# Package initialization
__init()
