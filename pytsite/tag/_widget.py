"""Tag Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import taxonomy as _taxonomy

class Cloud(_taxonomy.widget.Cloud):
    """Tags Cloud Widget.
    """
    def __init__(self, **kwargs):
        super().__init__('tag', **kwargs)
