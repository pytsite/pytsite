"""Auth UI.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

__import__('pytsite.odm_ui')
__import__('pytsite.file')

from pytsite.core import router, lang, odm
from pytsite import admin
from .models import UserUI, RoleUI

lang.register_package(__name__)

# Replace 'user' model with UI-compatible
odm.manager.register_model('user', UserUI, True)
odm.manager.register_model('role', RoleUI, True)

# 'Security' admin sidebar section
admin.sidebar.add_section('auth', 'pytsite.auth_ui@security', 1000,
                    permissions=('pytsite.odm_ui.browse.user', 'pytsite.odm_ui.browse.role'))

# 'Users' admin sidebar menu
url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': 'user'})
admin.sidebar.add_menu('auth', 'users', 'pytsite.auth_ui@users', url, 'fa fa-user', weight=10,
                 permissions=('pytsite.odm_ui.browse.user',))

# 'Roles' admin sidebar menu
url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': 'role'})
admin.sidebar.add_menu('auth', 'roles', 'pytsite.auth_ui@roles', url, 'fa fa-users', weight=20,
                 permissions=('pytsite.odm_ui.browse.role',))
