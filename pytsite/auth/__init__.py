""" PytSite Auth Module Init.
"""
# Public API
from . import _error as error, _functions, _model as model
from ._functions import define_permission_group,  define_permission, get_current_user, get_permission, \
    get_permission_groups, get_permissions, get_user_statuses, get_permission_group, get_user, create_user, get_role, \
    get_login_form, find_users

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def __init():
    """Init wrapper.
    """
    import sys
    from pytsite import reg, assetman, odm, events, tpl, lang, router, robots
    from . import _eh

    # Resources
    tpl.register_package(__name__)
    tpl.register_global('auth', sys.modules[__name__])
    lang.register_package(__name__)
    assetman.register_package(__name__)

    # ODM models
    from . import _model
    odm.register_model('user', _model.User)
    odm.register_model('role', _model.Role)

    # Routes
    base_path = reg.get('auth.base_path', '/auth')
    router.add_rule(base_path + '/login', __name__ + '.ep.login')
    router.add_rule(base_path + '/login/post', __name__ + '.ep.login_submit', methods='POST')
    router.add_rule(base_path + '/logout', __name__ + '.ep.logout')

    # Default auth driver
    from . import _functions
    from .driver.ulogin import ULoginDriver
    _functions.set_driver(ULoginDriver())

    # Template engine globals
    tpl.register_global('auth', _functions)

    # Event handlers
    events.listen('pytsite.setup', _eh.app_setup)
    events.listen('pytsite.router.dispatch', _eh.router_dispatch)
    events.listen('pytsite.update', _eh.update)

    # Permissions
    _functions.define_permission_group('auth', 'pytsite.auth@auth_permission_group_description')
    _functions.define_permission('admin', 'pytsite.auth@admin_permission_description', 'auth')

    # robots.txt rules
    robots.disallow(base_path + '/')


__init()
