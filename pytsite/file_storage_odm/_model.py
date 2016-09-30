"""PytSite File ODM Storage Models.
"""
import exifread as _exifread
from os import unlink as _unlink, path as _path
from PIL import Image as _PILImage
from pytsite import odm as _odm, reg as _reg, router as _router, file as _file
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AnyFileODMEntity(_odm.model.Entity):
    """Any File ODM Model.
    """
    _collection_name = 'file_other'

    def _setup_fields(self):
        """_setup() hook.
        """
        self.define_field(_odm.field.String('path', required=True))
        self.define_field(_odm.field.String('name', required=True))
        self.define_field(_odm.field.String('description'))
        self.define_field(_odm.field.String('mime', required=True))
        self.define_field(_odm.field.Integer('length', required=True))
        self.define_field(_odm.field.Virtual('local_path'))
        self.define_field(_odm.field.Virtual('url'))
        self.define_field(_odm.field.Virtual('thumb_url'))

    def _after_delete(self, **kwargs):
        """_after_delete() hook.
        """
        # Remove file from the storage
        local_path = self.f_get('local_path')
        if _path.exists(local_path):
            _unlink(local_path)

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        # Absolute file path on the filesystem
        if field_name == 'local_path':
            return _path.join(_reg.get('paths.storage'), self.f_get('path'))

        # File download URL
        elif field_name == 'url':
            p = self.f_get('path').split('/')
            return _router.ep_url('pytsite.file@download', {
                'model': p[0],
                'p1': p[1],
                'p2': p[2],
                'filename': p[3]
            })

        # File thumbnail/icon download URL
        elif field_name == 'thumb_url':
            raise NotImplementedError()

        else:
            return super()._on_f_get(field_name, value, **kwargs)

    def as_jsonable(self, **kwargs):
        """Hook.
        """
        r = super().as_jsonable(**kwargs)

        r.update({
            'name': self.f_get('name'),
            'description': self.f_get('description'),
            'mime': self.f_get('mime'),
            'length': self.f_get('length'),
            'url': self.f_get('url'),
            'thumb_url': self.f_get('thumb_url'),
        })

        return r


class ImageFileODMEntity(AnyFileODMEntity):
    """Image File ODM Model.
    """
    _collection_name = 'file_images'

    def _setup_fields(self):
        """Hook.
        """
        super()._setup_fields()
        self.define_field(_odm.field.Integer('width'))
        self.define_field(_odm.field.Integer('height'))
        self.define_field(_odm.field.Dict('exif'))

    def _pre_save(self, **kwargs):
        """Hook.
        """
        super()._pre_save(**kwargs)

        # Read EXIF from file
        with open(self.f_get('local_path'), 'rb') as f:
            exif = _exifread.process_file(f, details=False)
            entity_exif = {}
            for k, v in exif.items():
                if not k.startswith('Thumbnail'):
                    entity_exif[k] = str(v)
            self.f_set('exif', entity_exif)

        # Open image for processing
        image = _PILImage.open(self.f_get('local_path'))  # type: _PILImage.Image

        # Rotate image
        if 'Image Orientation' in exif:
            orientation = str(exif['Image Orientation'])
            rotated = None
            if orientation == 'Rotated 90 CCW':
                rotated = image.rotate(90, _PILImage.BICUBIC, True)
            elif orientation == 'Rotated 90 CW':
                rotated = image.rotate(-90, _PILImage.BICUBIC, True)
            elif orientation == 'Rotated 180':
                rotated = image.rotate(180, _PILImage.BICUBIC, True)

            if rotated:
                rotated.save(self.f_get('local_path'))
                image = rotated

        # Convert BMP to JPEG
        if image.format == 'BMP':
            current_local_path = self.f_get('local_path')

            # Change path and MIME info
            new_path = self.f_get('path').replace('.bmp', '.jpg')
            if not new_path.endswith('.jpg'):
                new_path += '.jpg'
            self.f_set('path', new_path)
            self.f_set('mime', 'image/jpeg')

            image.save(self.f_get('local_path'))
            _unlink(current_local_path)

        self.f_set('width', image.size[0])
        self.f_set('height', image.size[1])

        image.close()

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'url':
            try:
                width = abs(int(kwargs.get('width', 0)))
                height = abs(int(kwargs.get('height', 0)))
                if width or height:
                    if width:
                        width = _api.align_image_side(width, _api.get_image_resize_limit_width())
                    if height:
                        height = _api.align_image_side(height, _api.get_image_resize_limit_height())

            except ValueError:
                raise ValueError('Width and height should be positive integers.')

            uid = str(self.id)
            extension = _path.splitext(self.f_get('path'))[1]
            return _router.ep_url('pytsite.file_storage_odm@image', {
                'width': width,
                'height': height,
                'p1': uid[:2],
                'p2': uid[2:4],
                'filename': '{}{}'.format(uid, extension)
            }, strip_lang=True)

        elif field_name == 'thumb_url':
            return self.f_get('url', width=kwargs.get('width', 450), height=kwargs.get('height', 450))

        else:
            return super()._on_f_get(field_name, value, **kwargs)

    def _on_f_set(self, field_name: str, value, **kwargs):
        if field_name == 'local_path':
            raise RuntimeError('Local path of the file cannot be changed.')

        return super()._on_f_set(field_name, value, **kwargs)


class AnyFile(_file.model.AbstractFile):
    """Any File Model.
    """

    def __init__(self, entity: AnyFileODMEntity):
        """Init.
        """
        if not isinstance(entity, AnyFileODMEntity):
            raise TypeError('AnyFileODMEntity instance expected, got {}.'.format(type(entity)))

        self._entity = entity

    @property
    def uid(self) -> str:
        return str(self._entity.ref_str)

    def get_field(self, field_name: str, **kwargs):
        return self._entity.f_get(field_name, **kwargs)

    def set_field(self, field_name: str, value, **kwargs):
        return self._entity.f_set(field_name, value, **kwargs)

    def save(self):
        with self._entity as e:
            e.save()

    def delete(self):
        with self._entity as e:
            e.delete()


class ImageFile(_file.model.AbstractImage):
    """Imge File Model.
    """

    def __init__(self, entity: ImageFileODMEntity):
        if not isinstance(entity, ImageFileODMEntity):
            raise TypeError('ImageFileODMEntity instance expected, got {}.'.format(type(entity)))

        self._entity = entity

    @property
    def uid(self) -> str:
        return str(self._entity.ref_str)

    def get_field(self, field_name: str, **kwargs):
        return self._entity.f_get(field_name, **kwargs)

    def set_field(self, field_name: str, value, **kwargs):
        return self._entity.f_set(field_name, value, **kwargs)

    def save(self):
        with self._entity as e:
            e.save()

    def delete(self):
        with self._entity as e:
            e.delete()
