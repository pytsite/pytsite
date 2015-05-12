"""Image manager.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from .models import Image


def create(source_path: str, name: str=None, description: str=None)->Image:
    """Create an image from URL or local file.
    """
    from PIL import Image
    from ..file import manager as file_manager
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