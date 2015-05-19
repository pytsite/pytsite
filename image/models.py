"""Image model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path
from pytsite.core.odm.fields import IntegerField
from pytsite.file.models import File
from pytsite.core.router import endpoint_url


class Image(File):
    """Image model.
    """

    def get_thumbnail_url(self, width: int=64, height: int=64) -> str:
        """Get image's thumbnail URL.
        """

        p1, p2, filename = self.f_get('path').split(path.sep)

        return endpoint_url('pytsite.image.endpoints.get_resize',
                            {'width': width, 'height': height, 'p1': p1, 'p2': p2, 'filename': filename})

    def _setup(self):
        """_setup() hook.
        """

        super()._setup()
        self.define_field(IntegerField('width'))
        self.define_field(IntegerField('height'))
