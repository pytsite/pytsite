from pytsite import routing as _routing, metatag as _metatag, lang as _lang
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Dashboard(_routing.Controller):
    """Dashboard controller
    """

    def exec(self):
        _metatag.t_set('title', _lang.t('pytsite.admin@dashboard'))

        return _api.render('')
