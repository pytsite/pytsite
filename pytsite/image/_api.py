"""Image manager.
"""
from typing import Union as _Union
from PIL import Image
from bson.dbref import DBRef as _DBRef
from pytsite import file as _file, auth as _auth
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def create(source: str, name: str=None, description: str=None, remove_source: bool=False,
           propose_store_path: str=None, owner: _auth.model.AbstractUser = None) -> _model.Image:
    """Create an image from URL or local file.
    """
    img_entity = _file.create(source, name, description, 'image', remove_source, propose_store_path, owner)

    if not img_entity.mime.startswith('image'):
        with img_entity:
            img_entity.delete()
        raise ValueError("'{}' is not a acceptable type for image.".format(img_entity.mime))

    img_obj = Image.open(img_entity.abs_path)
    size = img_obj.size
    img_obj.close()

    with img_entity:
        img_entity.f_set('width', size[0]).f_set('height', size[1]).save()

    return img_entity


def get(uid: str=None, rel_path: str=None) -> _model.Image:
    """Get image by UID or by relative path.
    """
    return _file.get(uid, rel_path, 'image')


def get_by_ref(ref: _Union[str, _DBRef]) -> _model.Image:
    """Get image by reference.
    """
    file = _file.get_by_ref(ref)
    if file.model != 'image':
        raise RuntimeError('File is not an image.')

    return file
