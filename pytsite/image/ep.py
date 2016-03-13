"""Image Endpoints.
"""
from os import path as _path, makedirs as _makedirs
from math import floor as _floor
from PIL import Image as _Image
from pytsite import reg as _reg, http as _http, router as _router
from . import _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def resize(args: dict, inp: dict) -> _http.response.Redirect:
    requested_width = int(args['width'])
    requested_height = int(args['height'])
    file_path = _path.join('image', args['p1'], args['p2'], args['filename'])

    image_entity = _api.get(rel_path=file_path)
    if not image_entity:
        raise _http.error.NotFound()

    # Aligning side lengths
    aligned_width = _align_length(requested_width, int(_reg.get('image.resize_limit_width', 1200)))
    aligned_height = _align_length(requested_height, int(_reg.get('image.resize_limit_height', 1200)))
    if aligned_width != requested_width or aligned_height != requested_height:
        redirect = _router.ep_url('pytsite.image.ep.resize', {
            'width': aligned_width,
            'height': aligned_height,
            'p1': args['p1'],
            'p2': args['p2'],
            'filename': args['filename'],
        })
        return _http.response.Redirect(redirect, 301)

    # Original size
    orig_width = image_entity.width
    orig_height = image_entity.height
    orig_ratio = orig_width / orig_height

    need_resize = True

    # Calculate new size
    if not requested_width and not requested_height:
        # No resize needed, return original image
        resize_width = orig_width
        resize_height = orig_height
        need_resize = False
    elif requested_width and not requested_height:
        # Resize by width, preserve aspect ration
        resize_width = requested_width
        resize_height = _floor(requested_width / orig_ratio)
    elif requested_height and not requested_width:
        # Resize by height, preserve aspect ration
        resize_width = _floor(requested_height * orig_ratio)
        resize_height = requested_height
    else:
        # Exact resizing
        resize_width = requested_width
        resize_height = requested_height

    # Checking source file
    source_path = image_entity.path
    source_abs_path = image_entity.abs_path
    if not _path.exists(source_abs_path):
        return _http.response.Redirect('http://placehold.it/{}x{}'.format(requested_width, requested_height))

    # Calculating target file location
    target_abs_path = _path.join(_reg.get('paths.static'), 'image', 'resize', str(requested_width),
                                 str(requested_height), source_path.replace('image' + _path.sep, ''))
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
            image = cropped.resize((resize_width, resize_height), _Image.BILINEAR)

        image.save(target_abs_path)
        image.close()

    return _http.response.Redirect(image_entity.f_get('url', width=requested_width, height=requested_height))


def _align_length(l: int, max_length: int=2000, step: int=50):
    if l <= 0:
        return 0

    for n in range(0, max_length, step):
        if l <= n:
            return n

    return max_length
