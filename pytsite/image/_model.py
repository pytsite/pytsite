"""Image Models.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import file
from pytsite.core import odm, router


class Image(file.model.File):
    """Image Model.
    """

    def _setup(self):
        """Hook.
        """
        super()._setup()
        self._define_field(odm.field.Integer('width'))
        self._define_field(odm.field.Integer('height'))
        self._define_field(odm.field.Dict('exif'))

    def _pre_save(self):
        """Hook.
        """
        import exifread
        with open(self.f_get('abs_path'), 'rb') as f:
            exif = exifread.process_file(f, details=False)
            entity_exif = {}
            for k, v in exif.items():
                if not k.startswith('Thumbnail'):
                    entity_exif[k] = str(v)
            self.f_set('exif', entity_exif)

        from PIL import Image as PILImage
        image = PILImage.open(self.f_get('abs_path'))
        """:type: PIL.Image.Image"""

        # Rotate image
        if 'Image Orientation' in exif:
            orientation = str(exif['Image Orientation'])
            rotated = None
            if orientation == 'Rotated 90 CCW':
                rotated = image.rotate(270, PILImage.BICUBIC, True)
            elif orientation == 'Rotated 90 CW':
                rotated = image.rotate(90, PILImage.BICUBIC, True)
            elif orientation == 'Rotated 180':
                rotated = image.rotate(180, PILImage.BICUBIC, True)

            if rotated:
                image.close()
                rotated.save(self.f_get('abs_path'))
                image = rotated

        self.f_set('width', image.size[0])
        self.f_set('height', image.size[1])

        image.close()

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'url':
            from os import path
            p = str(self.f_get('path')).split(path.sep)

            return router.endpoint_url('pytsite.image.eps.get_resize', {
                'width': int(kwargs.get('width', 0)),
                'height': int(kwargs.get('height', 0)),
                'p1': p[1],
                'p2': p[2],
                'filename': p[3]
            })

        if field_name == 'thumb_url':
            return self.f_get('url', width=int(kwargs.get('width', 422)), height=int(kwargs.get('height', 422)))

        return super()._on_f_get(field_name, value, **kwargs)
