"""oAuth Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import widget as _widget
from . import _functions

class ProviderSelect(_widget.select.Select):
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        for k, v in _functions.get_drivers().items():
            self._items.append((k, v[0]))
