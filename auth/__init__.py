__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from ..core import odm, router
from . import models

odm.register_model('user', models.User)

router.add_rule('/auth/login', __name__ + '.views.get_login', [], ['GET'])