"""oAuth Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import odm_ui
from pytsite.core import widget as _widget
from . import _functions


class ProviderSelect(_widget.select.Select):
    """oAuth Provider Select Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        for k, v in _functions.get_drivers().items():
            self._items.append((k, v[0]))


class AccountSelect(odm_ui.widget.ODMSelect):
    """oAuth Account Select Widget.
    """
    def __init__(self, **kwargs: dict):
        self._model = 'oauth_account'
        self._caption_field = 'fqsn'
        self._sort_field = 'screen_name'
        super().__init__(**kwargs)
