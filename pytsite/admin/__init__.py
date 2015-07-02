"""Admin Package Init
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    from pytsite.core import router, tpl, assetman, lang, client
    from pytsite import auth
    from . import _sidebar

    lang.register_package(__name__)
    tpl.register_package(__name__)
    assetman.register_package(__name__)

    # Permissions
    auth.define_permission_group('admin', 'pytsite.admin@admin')
    auth.define_permission('admin.use', 'pytsite.admin@use_admin_panel', 'admin')

    # Routes
    admin_route_filters = (
        'pytsite.auth.eps.filter_authorize:permissions=admin.use',
    )
    router.add_rule('/admin', __name__ + '.eps.dashboard', filters=admin_route_filters)

    client.include('bootstrap', '/admin*')
    client.include('font-awesome', '/admin*')

    _sidebar.add_section('misc', 'pytsite.admin@miscellaneous', 500, ('*',))

# Initialization
__init()

# Public API
from . import _sidebar, _navbar
sidebar = _sidebar
navbar = _navbar
