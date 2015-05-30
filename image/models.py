"""Image model.
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
    """Image model.
    """

    def _setup(self):
        """_setup() hook.
        """

        super()._setup()
        self.define_field(IntegerField('width'))
        self.define_field(IntegerField('height'))

    def _pre_save(self):
        image = PILImage.open(self.f_get('abs_path'))
        self.f_set('width', image.size[0])
        self.f_set('height', image.size[1])

    def _on_f_get(self, field_name: str, orig_value, **kwargs):
        """_on_f_get() hook.
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
            return self.f_get('url', height=int(kwargs.get('height', 256)))

        return super()._on_f_get(field_name, orig_value, **kwargs)
