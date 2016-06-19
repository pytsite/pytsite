"""PytSIte Authentication ODM Storage Driver.
"""
from . import _model as model
from ._driver import Driver

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _init():
    from pytsite import odm, lang, router, admin

    # Resources
    lang.register_package(__name__)

    # ODM models
    odm.register_model('user', model.User)
    odm.register_model('role', model.Role)

    # 'Security' admin sidebar section
    if not admin.sidebar.get_section('auth'):
        admin.sidebar.add_section('auth', 'pytsite.auth_storage_odm@security', 1000,
                                  permissions=('pytsite.odm_perm.view.user', 'pytsite.odm_perm.view.role'))

    # 'Users' admin sidebar menu
    url = router.ep_url('pytsite.odm_ui@browse', {'model': 'user'})
    admin.sidebar.add_menu('auth', 'users', 'pytsite.auth_storage_odm@users', url, 'fa fa-user', weight=10,
                           permissions=('pytsite.odm_perm.view.user',))

    # 'Roles' admin sidebar menu
    url = router.ep_url('pytsite.odm_ui@browse', {'model': 'role'})
    admin.sidebar.add_menu('auth', 'roles', 'pytsite.auth_storage_odm@roles', url, 'fa fa-users', weight=20,
                           permissions=('pytsite.odm_perm.view.role',))


_init()
