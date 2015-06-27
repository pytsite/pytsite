__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

def __init():
    """Init wrapper.
    """
    # Requirements
    __import__('pytsite.image')

    # Other imports
    from pytsite.core import router, tpl, events, lang, odm

    # Resources
    tpl.register_package(__name__)
    lang.register_package(__name__)

    # ODM models
    from . import _model
    odm.register_model('user', _model.User)
    odm.register_model('role', _model.Role)

    # Routes
    router.add_rule('/auth/login', __name__ + '.eps.get_login', {})
    router.add_rule('/auth/login/post', __name__ + '.eps.post_login', {}, ('POST',))
    router.add_rule('/auth/logout', __name__ + '.eps.get_logout', {})

    # Default auth driver
    from . import _functions
    from .driver.ulogin import ULoginDriver
    _functions.set_driver(ULoginDriver())

    # Template engine globals
    tpl.register_global('auth', _functions)

    # Event handlers
    from ._event_handlers import app_setup
    events.listen('app.setup', app_setup)

    # Permissions
    _functions.define_permission_group('auth', 'pytsite.auth@auth_permission_group_description')
    _functions.define_permission('admin', 'pytsite.auth@admin_permission_description', 'auth')


__init()


# Public API
from . import _error, _functions, _model
error = _error
model = _model

from ._functions import define_permission_group,  define_permission, get_current_user, get_permission, \
    get_permission_groups, get_permissions, get_user_statuses, get_permission_group
