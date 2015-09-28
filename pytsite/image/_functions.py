"""Image manager.
"""
from PIL import Image
from pytsite import file as _file
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def create(source_path: str, name: str=None, description: str=None, remove_source: bool=False,
           propose_store_path: str=None) -> _model.Image:
    """Create an image from URL or local file.
    """
    img_entity = _file.functions.create(source_path, name, description, 'image', remove_source, propose_store_path)

    mime = str(img_entity.f_get('mime'))
    if not mime.endswith(('png', 'jpeg', 'gif')):
        img_entity.delete()
        raise ValueError("'{}' is not a acceptable type for image.".format(mime))

    img_obj = Image.open(img_entity.f_get('abs_path'))
    size = img_obj.size
    img_obj.close()

    return img_entity.f_set('width', size[0]).f_set('height', size[1]).save()


def get(uid: str=None, rel_path: str=None) -> _model.Image:
    """Get image.
    """
    return _file.functions.get(uid, rel_path, 'image')
