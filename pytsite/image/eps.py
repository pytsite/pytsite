"""Image views.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from os import path, makedirs
from math import floor
from PIL import Image
from pytsite.core import reg, http
from . import _manager


def get_resize(args: dict, inp: dict) -> http.response.RedirectResponse:
    requested_width = args['width']
    requested_height = args['height']
    file_path = path.join('image', args['p1'], args['p2'], args['filename'])

    image_entity = _manager.get(rel_path=file_path)
    if not image_entity:
        raise http.error.NotFoundError()

    # Sizes cannot be negative
    requested_width = requested_width if requested_width >= 0 else 0
    requested_height = requested_height if requested_height >= 0 else 0

    # Maximum resize sizes
    max_width = int(reg.get('image.resize.limit.width', 2000))
    requested_width = requested_width if requested_width <= max_width else max_width
    max_height = int(reg.get('image.resize.limit.height', 2000))
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
        resize_height = floor(requested_width / orig_ratio)
    elif requested_height and not requested_width:
        resize_width = floor(requested_height * orig_ratio)
        resize_height = requested_height
    else:
        resize_width = requested_width
        resize_height = requested_height

    # Checking source file
    source_path = image_entity.f_get('path')
    source_abs_path = image_entity.f_get('abs_path')
    if not path.exists(source_abs_path):
        return http.response.RedirectResponse('http://placehold.it/{}x{}'.format(requested_width, requested_height))

    # Calculating target file location
    target_abs_path = path.join(reg.get('paths.static'), 'image', 'resize', str(requested_width), str(requested_height),
                                str(source_path).replace('image' + path.sep, ''))
    target_dir = path.dirname(target_abs_path)
    if not path.exists(target_dir):
        makedirs(target_dir, 0o755, True)

    if not path.exists(target_abs_path):
        # Open source image
        image = Image.open(source_abs_path)
        """:type : PIL.Image.Image"""

        # Resize
        if need_resize:
            # Crop
            crop_ratio = resize_width / resize_height
            crop_width = orig_width
            crop_height = floor(crop_width / crop_ratio)
            crop_top = floor(orig_height / 2) - floor(crop_height / 2)
            crop_left = 0
            if crop_height > orig_height:
                crop_height = orig_height
                crop_width = floor(crop_height * crop_ratio)
                crop_top = 0
                crop_left = floor(orig_width / 2) - floor(crop_width / 2)
            crop_right = crop_left + crop_width
            crop_bottom = crop_top + crop_height

            cropped = image.crop((crop_left, crop_top, crop_right, crop_bottom))
            image.close()

            # Resize
            resized = cropped.resize((resize_width, resize_height))
            image = resized

        image.save(target_abs_path)
        image.close()

    return http.response.RedirectResponse(image_entity.f_get('url', width=requested_width, height=requested_height))
