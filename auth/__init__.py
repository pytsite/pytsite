__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Requirements
__import__('pytsite.image')
__import__('pytsite.jquery')

# Other imports
from pytsite.core import odm, router, tpl, lang, events

# Resources
tpl.register_package(__name__)
lang.register_package(__name__)

# ODM models
from . import models
odm.manager.register_model('user', models.User)
odm.manager.register_model('role', models.Role)

# Routes
router.add_rule('/auth/login', __name__ + '.endpoints.get_login', {}, ['GET'])
router.add_rule('/auth/login/post', __name__ + '.endpoints.post_login', {}, ['GET'])
router.add_rule('/auth/logout', __name__ + '.endpoints.get_logout', {}, ['GET'])

# Default auth driver
from . import manager
from .drivers.ulogin import ULoginDriver
manager.set_driver(ULoginDriver())

# Event handlers
from .event_handlers import app_setup
events.listen('app.setup', app_setup)

# Permissions
manager.define_permission('admin', 'pytsite.auth@admin_permission_description')
