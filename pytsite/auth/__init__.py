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
    odm.manager.register_model('user', _model.User)
    odm.manager.register_model('role', _model.Role)

    # Routes
    router.add_rule('/auth/login', __name__ + '.eps.get_login', {})
    router.add_rule('/auth/login/post', __name__ + '.eps.post_login', {}, ('POST',))
    router.add_rule('/auth/logout', __name__ + '.eps.get_logout', {})

    # Default auth driver
    from . import _manager
    from .driver.ulogin import ULoginDriver
    _manager.set_driver(ULoginDriver())

    # Template engine globals
    tpl.register_global('auth', _manager)

    # Event handlers
    from ._event_handlers import app_setup
    events.listen('app.setup', app_setup)

    # Permissions
    _manager.define_permission_group('auth', 'pytsite.auth@auth_permission_group_description')
    _manager.define_permission('admin', 'pytsite.auth@admin_permission_description', 'auth')


__init()


# Public API
from . import _error, _manager, _model
error = _error
manager = _manager
model = _model
