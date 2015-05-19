__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Requirements
__import__('pytsite.tbootstrap')
__import__('pytsite.fontawesome')
__import__('pytsite.auth')

# Other imports
from pytsite.core import lang, router, tpl, assetman
from pytsite.auth import manager as auth

lang.register_package(__name__)
tpl.register_package(__name__)
assetman.register_package(__name__)

admin_route_filters = (
    'pytsite.auth.endpoints.filter_authorize:permissions=admin.use',
)
router.add_rule('/admin', __name__ + '.endpoints.dashboard', filters=admin_route_filters)

auth.define_permission('admin.use', lang.t('pytsite.admin@use_admin_panel'))
