"""Image manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from PIL import Image
from pytsite.file import manager as file_manager
from .models import Image as ImageModel


def get_storage_root() -> str:
    """Get image storage root.
    """

    return file_manager.get_storage_root('image')


def create(source_path: str, name: str=None, description: str=None) -> ImageModel:
    """Create an image from URL or local file.
    """

    img_entity = file_manager.create(source_path, name, description, 'image')

    mime = str(img_entity.f_get('mime'))
    if not mime.endswith(('png', 'jpeg', 'gif')):
        img_entity.delete()
        raise ValueError("'{0}' is not a acceptable type for image.".format(mime))

    img_obj = Image.open(img_entity.f_get('abs_path'))
    size = img_obj.size
    img_obj.close()
    img_entity.f_set('width', size[0])
    img_entity.f_set('height', size[1])
    img_entity.save()

    return img_entity


def get(uid: str=None, rel_path: str=None) -> ImageModel:
    """Get image.
    """

    return file_manager.get(uid, rel_path, 'image')
