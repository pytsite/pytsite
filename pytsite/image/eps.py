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
    width = args['width']
    height = args['height']
    file_path = path.join('image', args['p1'], args['p2'], args['filename'])

    image_entity = image_manager.get(rel_path=file_path)
    if not image_entity:
        raise NotFoundError()

    # Sizes cannot be negative
    width = width if width >= 0 else 0
    height = height if height >= 0 else 0

    # Maximum resize sizes
    max_width = int(reg.get('image.resize.limit.width', 2000))
    width = width if width <= max_width else max_width
    max_height = int(reg.get('image.resize.limit.height', 2000))
    height = height if height <= max_height else max_height

    target_width = width
    target_height = height

    # Original size
    orig_width = image_entity.f_get('width')
    orig_height = image_entity.f_get('height')
    size_ratio = orig_width / orig_height

    # Calculate size to preserve proportions
    if width and height:
        if width > height:
            height = floor(width / size_ratio)
        elif width <= height:
            width = floor(height * size_ratio)
    elif width and not height:
        height = floor(width / size_ratio)
    elif height and not width:
        width = floor(height * size_ratio)
    else:
        width = orig_width
        height = orig_height

    # Checking source file
    source_path = image_entity.f_get('path')
    source_abs_path = image_entity.f_get('abs_path')
    if not path.exists(source_abs_path):
        return RedirectResponse('http://placehold.it/{}x{}'.format(width, height))

    # Calculating target file position
    target_abs_path = path.join(reg.get('paths.static'), 'image', 'resize', str(width), str(height),
                                str(source_path).replace('image' + path.sep, ''))
    target_dir = path.dirname(target_abs_path)
    if not path.exists(target_dir):
        makedirs(target_dir, 0o755, True)

    # Resizing image
    if not path.exists(target_abs_path):
        image = Image.open(source_abs_path)
        """:type : PIL.Image.Image"""
        resized = image.resize((width, height))
        resized.save(target_abs_path)

    return RedirectResponse(image_entity.f_get('url', width=width, height=height))
