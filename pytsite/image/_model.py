"""Image Models.
"""
import exifread as _exifread
import os as _os
from pytsite import file as _file, odm as _odm, router as _router, util as _util

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Image(_file.model.File):
    """Image Model.
    """
    def _setup_fields(self):
        """Hook.
        """
        super()._setup_fields()
        self.define_field(_odm.field.Integer('width'))
        self.define_field(_odm.field.Integer('height'))
        self.define_field(_odm.field.Dict('exif'))

    @property
    def width(self) -> int:
        return self.f_get('width')

    @property
    def height(self) -> int:
        return self.f_get('height')

    @property
    def exif(self) -> dict:
        return self.f_get('exif')

    def _pre_save(self):
        """Hook.
        """
        # Read EXIF from file
        with open(self.f_get('abs_path'), 'rb') as f:
            exif = _exifread.process_file(f, details=False)
            entity_exif = {}
            for k, v in exif.items():
                if not k.startswith('Thumbnail'):
                    entity_exif[k] = str(v)
            self.f_set('exif', entity_exif)

        # Open image for processing
        from PIL import Image as PILImage
        image = PILImage.open(self.abs_path)
        """:type: PIL.Image.Image"""

        # Rotate image
        if 'Image Orientation' in exif:
            orientation = str(exif['Image Orientation'])
            rotated = None
            if orientation == 'Rotated 90 CCW':
                rotated = image.rotate(90, PILImage.BICUBIC, True)
            elif orientation == 'Rotated 90 CW':
                rotated = image.rotate(-90, PILImage.BICUBIC, True)
            elif orientation == 'Rotated 180':
                rotated = image.rotate(180, PILImage.BICUBIC, True)

            if rotated:
                rotated.save(self.f_get('abs_path'))
                image = rotated

        # Convert BMP to JPEG
        if image.format == 'BMP':
            current_abs_path = self.abs_path

            # Change path and MIME info
            new_path = self.path.replace('.bmp', '.jpg')
            if not new_path.endswith('.jpg'):
                new_path += '.jpg'
            self.f_set('path', new_path)
            self.f_set('mime', 'image/jpeg')

            image.save(self.abs_path)
            _os.remove(current_abs_path)

        self.f_set('width', image.size[0])
        self.f_set('height', image.size[1])

        image.close()

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'url':
            from os import path
            p = str(self.path).split(path.sep)

            return _router.ep_url('pytsite.image.ep.resize', {
                'width': int(kwargs.get('width', 0)),
                'height': int(kwargs.get('height', 0)),
                'p1': p[1],
                'p2': p[2],
                'filename': p[3]
            }, strip_lang=True)

        elif field_name == 'thumb_url':
            return self.f_get('url', width=int(kwargs.get('width', 450)), height=int(kwargs.get('height', 450)))
        else:
            return super()._on_f_get(field_name, value, **kwargs)

    def get_url(self, width: int=0, height: int=0) -> str:
        """Shortcut to use in Jinja templates.
        """
        return self.f_get('url', width=width, height=height)

    def get_html(self, alt: str= '', css: str= '', width: int=0, height: int=0, enlarge: bool=True):
        """Get HTML code to embed the image.
        """
        if not enlarge:
            if width and width > self.width:
                width = self.width
            if height and height > self.height:
                height = self.height

        css += ' img-responsive'

        return '<img src="{}" class="{}" alt="{}">'.format(
            self.get_url(width, height), css.strip(), _util.escape_html(alt)
        )

    def get_responsive_html(self, alt: str='', css: str='', aspect_ratio: float=None, enlarge: bool=True) -> str:
        """Get HTML code to embed the image (responsive way).
        """
        alt = _util.escape_html(alt)
        path = self.path.replace('image/', '')
        css += ' img-responsive pytsite-img'

        return '<span class="{}" data-path="{}" data-alt="{}" data-aspect-ratio="{}" ' \
               'data-width="{}" data-height="{}" data-enlarge="{}"></span>'\
            .format(css.strip(), path, alt, aspect_ratio, self.width, self.height, enlarge)
