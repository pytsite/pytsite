"""Currency Widgets
"""
from pytsite import widget as _widget
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Select(_widget.select.Select):
    """Currency Select Widget
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        all_c = sorted(_api.get_all())

        # Exclude 'system' currencies
        if kwargs.get('exclude_system', True):
            all_c = [c for c in all_c if not c.startswith('_')]

        # Exclude additional currencies
        all_c = [c for c in all_c if c not in kwargs.get('exclude', ())]

        self._items = zip(all_c, ['{} ({})'.format(c, _api.get_title(c)) for c in all_c])
