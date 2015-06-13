__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Requirements
__import__('pytsite.tbootstrap')
__import__('pytsite.auth')

from pytsite.core import router, tpl, assetman, lang
from pytsite.auth import auth_manager


lang.register_package(__name__)
tpl.register_package(__name__)
assetman.register_package(__name__)

# Permissions
auth_manager.define_permission_group('admin', 'pytsite.admin@admin')
auth_manager.define_permission('admin.use', 'pytsite.admin@use_admin_panel', 'admin')

# Routes
admin_route_filters = (
    'pytsite.auth.eps.filter_authorize:permissions=admin.use',
)
router.add_rule('/admin', __name__ + '.eps.dashboard', filters=admin_route_filters)
