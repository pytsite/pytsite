__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from ..core import lang, router, tpl, assetman
from .. import tbootstrap, fontawesome, auth

router.add_rule('/admin', __name__ + '.views@dashboard')
lang.register_package(__name__)
tpl.register_package(__name__)

assetman.register_package(__name__)
