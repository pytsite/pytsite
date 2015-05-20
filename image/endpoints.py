"""Image views.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from os import path, makedirs
from PIL import Image
from pytsite.core import reg
from pytsite.core.http.response import RedirectResponse
from pytsite.core.http.errors import NotFound
from . import image_manager


def get_resize(args: dict, inp: dict) -> RedirectResponse:
    width = args['width']
    height = args['height']
    file_path = path.join(args['p1'], args['p2'], args['filename'])

    image_entity = image_manager.get(rel_path=file_path)
    if not image_entity:
        raise NotFound()

    source_path = image_entity.f_get('path')
    source_abs_path = path.join(image_manager.get_storage_root(), source_path)

    if not path.exists(source_abs_path):
        return RedirectResponse('http://placehold.it/{}x{}'.format(width, height))

    target_abs_path = path.join(reg.get('paths.static'), 'image', 'resize', str(width), str(height), source_path)
    target_dir = path.dirname(target_abs_path)
    if not path.exists(target_dir):
        makedirs(target_dir, 0o755, True)

    image = Image.open(source_abs_path)
    """:type : PIL.Image.Image"""

    resized = image.resize((width, height))
    resized.save(target_abs_path)

    return RedirectResponse(image_entity.get_thumbnail_url(width, height), 301)
