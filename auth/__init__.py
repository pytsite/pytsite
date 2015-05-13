__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

import pytsite.image
from ..core import odm, router, tpl, lang
from . import manager, models
from .drivers.ulogin import ULoginDriver

odm.manager.register_model('user', models.User)

router.add_rule('/auth/login', __name__ + '.endpoints.get_login', {}, ['GET'])
router.add_rule('/auth/login/post', __name__ + '.endpoints.post_login', {}, ['POST'])

tpl.register_package(__name__)

lang.register_package(__name__)

manager.set_driver(ULoginDriver())