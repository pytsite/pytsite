"""PytSite ODM File Storage API Functions.
"""
from pytsite import reg as _reg

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_resize_limit_width = int(_reg.get('file_storage_odm.image_resize_limit_width', 1200))
_resize_limit_height = int(_reg.get('file_storage_odm.image_resize_limit_height', 1200))
_resize_step = int(_reg.get('file_storage_odm.image_resize_step', 50))


def get_image_resize_limit_width() -> int:
    return _resize_limit_width


def get_image_resize_limit_height() -> int:
    return _resize_limit_height


def get_image_resize_step() -> int:
    return _resize_step


def align_image_side(length: int, max_length: int, step: int = None) -> int:
    if not step:
        step = get_image_resize_step()

    if length <= 0:
        return 0

    if step in (0, 1):
        return length

    if length >= max_length:
        return max_length

    for n in range(0, max_length, step):
        if n >= length:
            return n

    return max_length
