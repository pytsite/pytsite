"""fb Package Event Handlers.
"""
from pytsite import metatag as _metatag, settings as _settings

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def router_dispatch():
    """'pytsite.router.dispatch' event handler.
    """
    _metatag.t_set('fb:app_id', _settings.get('fb.app_id'))
