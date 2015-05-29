"""Auth UI.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

__import__('pytsite.auth')
__import__('pytsite.odm_ui')
__import__('pytsite.file')

from pytsite.core import lang, router
from pytsite.core.odm import odm_manager
from pytsite.admin import sidebar
from .models import UserUI

lang.register_package(__name__)

# 'Security' admin sidebar section
sidebar.add_section('auth', lang.t('pytsite.auth_ui@security'), 1000)

# 'Users' admin sidebar menu
url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': 'user'})
sidebar.add_section_menu('auth', 'users', lang.t('pytsite.auth_ui@users'), url, 'fa fa-user', weight=10)

# 'Roles' admin sidebar menu
url = router.endpoint_url('pytsite.odm_ui.eps.browse', {'model': 'role'})
sidebar.add_section_menu('auth', 'roles', lang.t('pytsite.auth_ui@roles'), url, 'fa fa-users', weight=20)

# Replace 'user' model with UI-compatible
odm_manager.register_model('user', UserUI, True)
