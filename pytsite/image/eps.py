"""Image views.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from os import path, makedirs
from math import floor
from PIL import Image
from pytsite.core import reg
from pytsite.core.http.response import RedirectResponse
from pytsite.core.http.errors import NotFoundError
from . import image_manager


def get_resize(args: dict, inp: dict) -> RedirectResponse:
    requested_width = args['width']
    requested_height = args['height']
    file_path = path.join('image', args['p1'], args['p2'], args['filename'])

    image_entity = image_manager.get(rel_path=file_path)
    if not image_entity:
        raise NotFoundError()

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

    # Calculate size to preserve proportions
    resize_width = None
    resize_height = None
    prevent_crop = False
    if not requested_width and not requested_height:
        resize_width = orig_width
        resize_height = orig_height
    elif requested_width and not requested_height:
        resize_width = requested_width
        resize_height = floor(requested_width / orig_ratio)
        prevent_crop = True
    elif requested_height and not requested_width:
        resize_width = floor(requested_height * orig_ratio)
        resize_height = requested_height
        prevent_crop = True
    else:
        resize_width = requested_width
        resize_height = floor(requested_width / orig_ratio)

    # Checking source file
    source_path = image_entity.f_get('path')
    source_abs_path = image_entity.f_get('abs_path')
    if not path.exists(source_abs_path):
        return RedirectResponse('http://placehold.it/{}x{}'.format(requested_width, requested_height))

    # Calculating target file location
    target_abs_path = path.join(reg.get('paths.static'), 'image', 'resize', str(requested_width), str(requested_height),
                                str(source_path).replace('image' + path.sep, ''))
    target_dir = path.dirname(target_abs_path)
    if not path.exists(target_dir):
        makedirs(target_dir, 0o755, True)

    if not path.exists(target_abs_path):
        # Resizing image
        orig_image = Image.open(source_abs_path)
        """:type : PIL.Image.Image"""
        transformed = orig_image.resize((resize_width, resize_height))

        # Cropping image
        if not prevent_crop:
            if resize_height > requested_height:
                left = 0
                right = resize_width
                top = floor(resize_height / 2) - floor(requested_height / 2)
                bottom = top + requested_height
                transformed = transformed.crop((left, top, right, bottom))
            elif resize_height < requested_height:
                overlay = Image.new(transformed.mode, (requested_width, requested_height), '#ffffff')
                left = 0
                right = transformed.size[0]
                top = floor(overlay.size[1] / 2) - floor(transformed.size[1] / 2)
                bottom = top + transformed.size[1]
                overlay.paste(transformed, (left, top, right, bottom))
                transformed = overlay

        transformed.save(target_abs_path)

    return RedirectResponse(image_entity.f_get('url', width=requested_width, height=requested_height))
