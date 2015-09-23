"""Admin Package Init
"""
# Public API
from . import _sidebar as sidebar, _navbar as navbar

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def base_path() -> str:
    from pytsite import reg
    return reg.get('admin.base_path', '/admin')


def __init():
    """Init wrapper.
    """
    import sys
    from pytsite import assetman, tpl, lang, router, auth, robots

    lang.register_package(__name__)
    tpl.register_package(__name__)
    tpl.register_global('admin', sys.modules[__name__])
    assetman.register_package(__name__)

    # Permissions
    auth.define_permission_group('admin', 'pytsite.admin@admin')
    auth.define_permission('admin.use', 'pytsite.admin@use_admin_panel', 'admin')

    # Routes
    admin_route_filters = ('pytsite.auth.ep.filter_authorize:permissions=admin.use',)
    router.add_rule(base_path(), __name__ + '.ep.dashboard', filters=admin_route_filters)

    sidebar.add_section('misc', 'pytsite.admin@miscellaneous', 500)

    # robots.txt rules
    robots.disallow(base_path() + '/')

# Initialization
__init()
