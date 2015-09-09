"""Image Endpoints.
"""
from os import path as _path, makedirs as _makedirs
from math import floor as _floor
from PIL import Image as _Image
from pytsite import reg as _reg, http as _http
from . import _functions

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def resize(args: dict, inp: dict) -> _http.response.Redirect:
    requested_width = args['width']
    requested_height = args['height']
    file_path = _path.join('image', args['p1'], args['p2'], args['filename'])

    image_entity = _functions.get(rel_path=file_path)
    if not image_entity:
        raise _http.error.NotFound()

    # Sizes cannot be negative
    requested_width = requested_width if requested_width >= 0 else 0
    requested_height = requested_height if requested_height >= 0 else 0

    # Maximum resize sizes
    max_width = int(_reg.get('image.resize.limit.width', 2000))
    requested_width = requested_width if requested_width <= max_width else max_width
    max_height = int(_reg.get('image.resize.limit.height', 2000))
    requested_height = requested_height if requested_height <= max_height else max_height

    # Original size
    orig_width = image_entity.f_get('width')
    orig_height = image_entity.f_get('height')
    orig_ratio = orig_width / orig_height

    need_resize = True

    # Calculate size
    if not requested_width and not requested_height:
        resize_width = orig_width
        resize_height = orig_height
        need_resize = False
    elif requested_width and not requested_height:
        resize_width = requested_width
        resize_height = _floor(requested_width / orig_ratio)
    elif requested_height and not requested_width:
        resize_width = _floor(requested_height * orig_ratio)
        resize_height = requested_height
    else:
        resize_width = requested_width
        resize_height = requested_height

    # Checking source file
    source_path = image_entity.f_get('path')
    source_abs_path = image_entity.f_get('abs_path')
    if not _path.exists(source_abs_path):
        return _http.response.Redirect('http://placehold.it/{}x{}'.format(requested_width, requested_height))

    # Calculating target file location
    target_abs_path = _path.join(_reg.get('paths.static'), 'image', 'resize', str(requested_width),
                                 str(requested_height), str(source_path).replace('image' + _path.sep, ''))
    target_dir = _path.dirname(target_abs_path)
    if not _path.exists(target_dir):
        _makedirs(target_dir, 0o755, True)

    if not _path.exists(target_abs_path):
        # Open source image
        image = _Image.open(source_abs_path)
        """:type : PIL.Image.Image"""

        # Resize
        if need_resize:
            # Crop
            crop_ratio = resize_width / resize_height
            crop_width = orig_width
            crop_height = _floor(crop_width / crop_ratio)
            crop_top = _floor(orig_height / 2) - _floor(crop_height / 2)
            crop_left = 0
            if crop_height > orig_height:
                crop_height = orig_height
                crop_width = _floor(crop_height * crop_ratio)
                crop_top = 0
                crop_left = _floor(orig_width / 2) - _floor(crop_width / 2)
            crop_right = crop_left + crop_width
            crop_bottom = crop_top + crop_height

            cropped = image.crop((crop_left, crop_top, crop_right, crop_bottom))
            image.close()

            # Resize
            resized = cropped.resize((resize_width, resize_height), _Image.BILINEAR)
            image = resized

        image.save(target_abs_path)
        image.close()

    return _http.response.Redirect(image_entity.f_get('url', width=requested_width, height=requested_height))
