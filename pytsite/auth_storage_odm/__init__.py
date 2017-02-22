"""PytSIte Authentication ODM Storage Driver.
"""
# Public API
from . import _model as model, _field as field
from ._driver import Driver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import odm, lang, router, admin, auth

    # Resources
    lang.register_package(__name__)

    # ODM models
    odm.register_model('role', model.ODMRole)
    odm.register_model('user', model.ODMUser)

    # 'Security' admin sidebar section
    admin.sidebar.add_section('auth', 'pytsite.auth_storage_odm@security', 1000)

    # 'Users' admin sidebar menu
    url = router.ep_path('pytsite.odm_ui@browse', {'model': 'user'})
    admin.sidebar.add_menu('auth', 'users', 'pytsite.auth_storage_odm@users', url, 'fa fa-users', weight=10,
                           permissions='pytsite.odm_auth.view.user')

    # 'Roles' admin sidebar menu
    url = router.ep_path('pytsite.odm_ui@browse', {'model': 'role'})
    admin.sidebar.add_menu('auth', 'roles', 'pytsite.auth_storage_odm@roles', url, 'fa fa-key', weight=20,
                           permissions='pytsite.odm_auth.view.role')

    # Register storage driver
    auth.register_storage_driver(Driver())


_init()
