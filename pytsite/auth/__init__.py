__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Requirements
__import__('pytsite.image')

# Other imports
from pytsite.core import router, tpl, lang, events
from pytsite.core.odm import odm_manager

# Resources
tpl.register_package(__name__)
lang.register_package(__name__)

# ODM models
from . import models
odm_manager.register_model('user', models.User)
odm_manager.register_model('role', models.Role)

# Routes
router.add_rule('/auth/login', __name__ + '.eps.get_login', {}, ['GET'])
router.add_rule('/auth/login/post', __name__ + '.eps.post_login', {}, ['POST'])
router.add_rule('/auth/logout', __name__ + '.eps.get_logout', {}, ['GET'])

# Default auth driver
from . import auth_manager
from .drivers.ulogin import ULoginDriver
auth_manager.set_driver(ULoginDriver())

# Template engine globals
tpl.register_global('auth', auth_manager)

# Event handlers
from .event_handlers import app_setup
events.listen('app.setup', app_setup)

# Permissions
auth_manager.define_permission_group('auth', 'pytsite.auth@auth_permission_group_description')
auth_manager.define_permission('admin', 'pytsite.auth@admin_permission_description', 'auth')
