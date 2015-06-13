"""Image Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from os import path
from PIL import Image as PILImage
from pytsite.core.odm.fields import IntegerField
from pytsite.file.models import File
from pytsite.core.router import endpoint_url


class Image(File):
    """Image Model.
    """

    def _setup(self):
        """Hook.
        """
        super()._setup()
        self._define_field(IntegerField('width'))
        self._define_field(IntegerField('height'))

    def _pre_save(self):
        """Hook.
        """
        image = PILImage.open(self.f_get('abs_path'))
        self.f_set('width', image.size[0])
        self.f_set('height', image.size[1])

    def _on_f_get(self, field_name: str, orig_value, **kwargs):
        """Hook.
        """
        if field_name == 'url':
            p = str(self.f_get('path')).split(path.sep)

            return endpoint_url('pytsite.image.eps.get_resize', {
                'width': int(kwargs.get('width', 0)),
                'height': int(kwargs.get('height', 0)),
                'p1': p[1],
                'p2': p[2],
                'filename': p[3]
            })

        if field_name == 'thumb_url':
            return self.f_get('url', width=int(kwargs.get('width', 422)), height=int(kwargs.get('height', 422)))

        return super()._on_f_get(field_name, orig_value, **kwargs)
