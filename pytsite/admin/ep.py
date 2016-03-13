from pytsite import metatag as _metatag, lang as _lang
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def dashboard(args: dict, inp: dict):
    """Dashboard endpoint.
    """
    _metatag.t_set('title', _lang.t('pytsite.admin@dashboard'))

    return _api.render('')
