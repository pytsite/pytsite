"""Image manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from PIL import Image
from pytsite.file import file_manager as file_manager
from .models import Image as ImageModel


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

    return img_entity.f_set('width', size[0]).f_set('height', size[1]).save()


def get(uid: str=None, rel_path: str=None) -> ImageModel:
    """Get image.
    """

    return file_manager.get(uid, rel_path, 'image')
